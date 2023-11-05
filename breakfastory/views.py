from django.shortcuts import render, redirect

from .forms import MealTypeForm, EntryForm
from .models import MealType, Entry


def index(request):
    """The home page for Breakfastory"""
    return render(request, 'breakfastory/index.html')

def meal_types(request):
    """Show all meal types."""
    meal_types = MealType.objects.order_by('date_added')
    context = {'meal_types': meal_types}
    return render(request, 'breakfastory/meal_types.html', context)

def meal_type(request, meal_type_id):
    """Show a single meal type and all its entries."""
    meal_type = MealType.objects.get(id=meal_type_id)
    entries = meal_type.entry_set.order_by('-date_added')
    context = {'meal_type': meal_type, 'entries': entries}
    return render(request, 'breakfastory/meal_type.html', context)

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
    return render(request, 'breakfastory/new_meal_type.html', context)

def new_entry(request, meal_type_id):
    """Add a new entry for a particular meal type."""
    meal_type = MealType.objects.get(id=meal_type_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data = request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.meal_type = meal_type
            new_entry.save()
            return redirect('breakfastory:meal_type', meal_type_id)
        
    # Display a blank or invalid form.
    context = {'meal_type': meal_type, 'form': form}
    return render(request, 'breakfastory/new_entry.html', context)

def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    meal_type = entry.meal_type

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('breakfastory:meal_type', meal_type_id=meal_type.id)
        
    context = {'entry': entry, 'meal_type': meal_type, 'form': form}
    return render(request, 'breakfastory/edit_entry.html', context)
