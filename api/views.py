from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.permissions import AllowAny
import pandas as pd
import os
import re
import json

# Ensure 'serializers.py' exists in the same folder
from .serializers import FileUploadSerializer

# --- CONFIGURATION ---
EXCEL_FILE_PATH = 'Sample_data.xlsx'


# --- HELPER: SMART SUMMARY GENERATOR ---
def generate_smart_summary(df, query, metric_label, locations):
    if df.empty:
        return "No data available to generate a summary."

    years = df['year'].tolist()
    start_year, end_year = min(years), max(years)

    # Identify Trend
    trend = "stable"
    if len(df) > 1:
        col = next((c for c in df.columns if 'rate' in c or 'price' in c or 'sold' in c), None)
        if col:
            first = df.iloc[0][col]
            last = df.iloc[-1][col]
            if last > first:
                trend = "showing a **strong upward trend**"
            elif last < first:
                trend = "showing a **decline**"

    # Construct Natural Language Summary
    summary = (
        f"**Analysis Report for {', '.join(locations)}**\n\n"
        f"Analyzing the data from **{start_year} to {end_year}**, the market is {trend}. "
        f"This report is based on **{len(df)} data points**, highlighting key shifts in **{metric_label}**."
    )
    return summary


# --- 1. TEST API ---
@api_view(['GET'])
@permission_classes([AllowAny])
def test_api(request):
    return Response({"message": "Sigmavalue API is running!"})


# --- 2. UPLOAD VIEW ---
class UploadExcelView(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']
            try:
                with open(EXCEL_FILE_PATH, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)

                df = pd.read_excel(EXCEL_FILE_PATH)
                return Response({
                    "status": "success",
                    "message": "File uploaded successfully.",
                    "columns": list(df.columns),
                    "filename": uploaded_file.name
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- 3. ANALYZE QUERY ---
@api_view(['POST'])
@permission_classes([AllowAny])
def analyze_query(request):
    user_query = request.data.get('query', '').lower()

    # 1. Load Data
    if not os.path.exists(EXCEL_FILE_PATH):
        return Response({"error": "Dataset not found. Please upload a file first."}, status=404)

    try:
        df = pd.read_excel(EXCEL_FILE_PATH)
        df.columns = [str(c).strip().lower() for c in df.columns]
    except Exception as e:
        return Response({"error": f"Error reading Excel: {str(e)}"}, status=500)

    # 2. Detect Location Column
    loc_col = 'final location'
    if loc_col not in df.columns:
        possible = [c for c in df.columns if 'loc' in c or 'area' in c]
        if possible:
            loc_col = possible[0]
        else:
            return Response({"error": "Location column not found."}, status=500)

    # 3. Identify ALL Locations (Fuzzy Search)
    df[loc_col] = df[loc_col].astype(str).str.strip()
    available_locations = df[loc_col].unique()
    found_locations = []

    for loc in available_locations:
        loc_str = str(loc).lower()
        if loc_str in user_query:
            found_locations.append(loc)
        else:
            parts = loc_str.split()
            if len(parts) > 1 and parts[0] in user_query:
                found_locations.append(loc)

    found_locations = list(set(found_locations))

    if not found_locations:
        return Response({
            "summary": f"I couldn't identify any locations. Try asking about: {', '.join(available_locations[:3])}...",
            "chart_data": None,
            "table_data": []
        })

    # 4. Filter Data
    filtered_df = df[df[loc_col].isin(found_locations)].copy()

    # Last X Years Logic
    if 'year' in filtered_df.columns:
        year_match = re.search(r'last (\d+) years', user_query)
        if year_match:
            years_back = int(year_match.group(1))
            max_year = filtered_df['year'].max()
            min_year = max_year - years_back + 1
            filtered_df = filtered_df[filtered_df['year'] >= min_year]

    # 5. Determine Intent
    if any(word in user_query for word in ['demand', 'sales', 'sold', 'units', 'volume']):
        metric_col = 'flat_sold - igr'
        metric_label = "Units Sold (Demand)"
    else:
        metric_col = 'flat - weighted average rate'
        metric_label = "Price Per SqFt (INR)"

    if metric_col not in filtered_df.columns:
        metric_col = next((c for c in filtered_df.columns if 'rate' in c or 'price' in c), None)
        if not metric_col: return Response({"error": "Metric column not found."}, status=500)

    # 6. Prepare Chart Data
    pivot_df = filtered_df.pivot_table(index='year', columns=loc_col, values=metric_col)

    datasets = []
    colors = ['#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']

    for idx, loc in enumerate(pivot_df.columns):
        data_values = pivot_df[loc].fillna(0).astype(float).tolist()
        datasets.append({
            "label": loc,
            "data": data_values,
            "borderColor": colors[idx % len(colors)]
        })

    chart_data = {
        "labels": pivot_df.index.astype(str).tolist(),
        "datasets": datasets
    }

    # 7. Generate Summary
    summary = generate_smart_summary(filtered_df, user_query, metric_label, found_locations)

    # 8. Prepare Table Data (Safe JSON)
    table_json_str = filtered_df.head(20).to_json(orient='records', date_format='iso')
    table_data = json.loads(table_json_str)

    return Response({
        "summary": summary,
        "chart_data": chart_data,
        "table_data": table_data
    })