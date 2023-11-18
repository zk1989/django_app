from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .forms import MealTypeForm, EntryForm
from .models import MealType, Entry


def index(request):
    """The home page for Breakfastory"""
    return render(request, 'breakfastory/index.html')

@login_required
def meal_types(request):
    """Show all meal types."""
    meal_types = MealType.objects.filter(owner=request.user).order_by('date_added')
    context = {'meal_types': meal_types}
    return render(request, 'breakfastory/meal_types.html', context)

@login_required
def meal_type(request, meal_type_id):
    """Show a single meal type and all its entries."""
    meal_type = MealType.objects.get(id=meal_type_id)
    # Make sure the meal type belongs to the current user.
    check_meal_type_owner(request, meal_type)
    
    entries = meal_type.entry_set.order_by('-date_added')
    context = {'meal_type': meal_type, 'entries': entries}
    return render(request, 'breakfastory/meal_type.html', context)

@login_required
def new_meal_type(request):
    """Add a new meal type."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = MealTypeForm()
    else:
        # POST data submitted; process data.
        form = MealTypeForm(data = request.POST)
        if form.is_valid():
            new_meal_type = form.save(commit=False)
            new_meal_type.owner = request.user
            new_meal_type.save()
            return redirect('breakfastory:meal_types')
        
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'breakfastory/new_meal_type.html', context)

@login_required
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
            check_meal_type_owner(request, meal_type)
            new_entry.meal_type = meal_type
            new_entry.save()
            return redirect('breakfastory:meal_type', meal_type_id)
        
    # Display a blank or invalid form.
    context = {'meal_type': meal_type, 'form': form}
    return render(request, 'breakfastory/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry."""
    entry = Entry.objects.get(id=entry_id)
    meal_type = entry.meal_type
    check_meal_type_owner(request, meal_type)

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

def check_meal_type_owner(request, meal_type):
    if meal_type.owner != request.user:
        raise Http404
