from django.shortcuts import render, redirect

from .forms import MealTypeForm
from .models import MealType


def index(request):
    """The home page for Breakfastory"""
    return render(request, 'breakfastory/index.html')

def meal_types(request):
    """Show all meal types."""
    meal_types = MealType.objects.order_by('date_added')
    context = {'meal_types': meal_types}
    return render(request, 'breakfastory/mealtypes.html', context)

def meal_type(request, mealtype_id):
    """Show a single meal type and all its entries."""
    meal_type = MealType.objects.get(id=mealtype_id)
    entries = meal_type.entry_set.order_by('-date_added')
    context = {'meal_type': meal_type, 'entries': entries}
    return render(request, 'breakfastory/mealtype.html', context)

def new_meal_type(request):
    """Add a new meal type."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = MealTypeForm()
    else:
        # POST data submitted; process data.
        form = MealTypeForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('breakfastory:meal_types')
        
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'breakfastory/new_mealtype.html', context)
