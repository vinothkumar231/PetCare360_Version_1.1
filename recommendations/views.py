from django.shortcuts import render
from .utils import recommend_from_text

def home(request):
    recommendations = None
    query = ""
    
    if request.method == "POST":
        query = request.POST.get("symptom")
        recommendations = recommend_from_text(query, top_n=5).to_dict(orient="records")
    
    return render(request, "home.html", {"query": query, "recommendations": recommendations})
