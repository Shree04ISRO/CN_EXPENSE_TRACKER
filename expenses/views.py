from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from .models import Expense
from .forms import ExpenseForm
from .utils import predict_category
from datetime import date, timedelta
from collections import defaultdict
import csv

# ── Auth Views ──────────────────────────────────────────────

def signup_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('dashboard')
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ── Dashboard ────────────────────────────────────────────────

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    filter_type = request.GET.get('filter', '')
    today = date.today()

    if filter_type == 'today':
        expenses = expenses.filter(date=today)
    elif filter_type == 'week':
        expenses = expenses.filter(date__gte=today - timedelta(days=7))
    elif filter_type == 'month':
        expenses = expenses.filter(date__gte=today - timedelta(days=30))

    total = sum(e.amount for e in expenses)

    # Category-wise totals for pie chart
    cat_totals = defaultdict(float)
    for e in expenses:
        cat_totals[e.category] += float(e.amount)

    # Date-wise totals for bar chart
    date_totals = defaultdict(float)
    for e in expenses:
        date_totals[str(e.date)] += float(e.amount)

    return render(request, 'dashboard.html', {
        'expenses': expenses.order_by('-date'),
        'total': total,
        'filter': filter_type,
        'cat_labels': list(cat_totals.keys()),
        'cat_values': list(cat_totals.values()),
        'date_labels': list(date_totals.keys()),
        'date_values': list(date_totals.values()),
    })


# ── CRUD ─────────────────────────────────────────────────────

@login_required
def add_expense(request):
    form = ExpenseForm(request.POST or None)
    if form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        # Auto-predict category if not changed from default
        if expense.category == 'Other':
            expense.category = predict_category(expense.description)
        expense.save()
        return redirect('dashboard')
    return render(request, 'expense_form.html', {'form': form, 'action': 'Add'})


@login_required
def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    form = ExpenseForm(request.POST or None, instance=expense)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'expense_form.html', {'form': form, 'action': 'Edit'})


@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    expense.delete()
    return redirect('dashboard')


# ── Export ───────────────────────────────────────────────────

@login_required
def export_csv(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'
    writer = csv.writer(response)
    writer.writerow(['Description', 'Amount', 'Category', 'Date'])
    for e in expenses:
        writer.writerow([e.description, e.amount, e.category, e.date])
    return response


@login_required
def export_pdf(request):
    try:
        from reportlab.pdfgen import canvas as rl_canvas
        expenses = Expense.objects.filter(user=request.user).order_by('-date')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="expenses.pdf"'
        c = rl_canvas.Canvas(response)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, 800, "Smart Expense Tracker Report")
        c.setFont("Helvetica", 11)
        y = 760
        c.drawString(50, y, f"{'Description':<30} {'Amount':>10}  {'Category':<12} {'Date'}")
        y -= 20
        c.line(50, y, 550, y)
        y -= 15
        total = 0
        for e in expenses:
            if y < 60:
                c.showPage()
                y = 800
            c.drawString(50, y, f"{str(e.description):<30} {float(e.amount):>10.2f}  {e.category:<12} {e.date}")
            y -= 18
            total += float(e.amount)
        y -= 10
        c.line(50, y, 550, y)
        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, f"Total: ₹{total:.2f}")
        c.save()
        return response
    except ImportError:
        return HttpResponse("reportlab not installed. Run: pip install reportlab", status=500)
