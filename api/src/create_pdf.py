"""
Module for generate the PDF statistics
"""

from types import SimpleNamespace
from datetime import datetime, date
from collections import Counter
from io import BytesIO

# Third-party modules
from flask import render_template
from weasyprint import HTML

# Own Modules
from data_access import get_all_users

def generate_statistics_pdf():
    """
    Generates statistics and creates a PDF
    """
    users = get_all_users()
    stats = calculate_statistics(users)
    current_date = datetime.now().strftime("%d.%m.%Y")

    # Rendert html zur Vorbereitung zum pdf
    html_content = render_template('pdf_template.html', stats=stats, current_date=current_date)
    
    # PDF generieren
    pdf_buffer = BytesIO()
    HTML(string=html_content).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)
    
    return pdf_buffer.getvalue()


def calculate_statistics(users):
    """
    Calculates various statistics from the list of persons
    """
    stats = SimpleNamespace()
    
    # Grundlegende Zahlen
    stats.total_persons = len(users)
    
    if stats.total_persons == 0:
        return stats

    # Kontakt- und Adressdaten
    stats.persons_with_contact = sum(1 for p in users if p.kontakt is not None)
    stats.persons_with_address = sum(1 for p in users if p.adresse is not None)

    # Altersberechnung
    today = date.today()
    ages = []
    stats.youngest = None
    stats.oldest = None
    stats.youngest_age = float("inf")
    stats.oldest_age = 0

    for user in users:
        if user.geburtsdatum:
            age = today.year - user.geburtsdatum.year
            if today.month < user.geburtsdatum.month or \
               (today.month == user.geburtsdatum.month and today.day < user.geburtsdatum.day):
                age -= 1

            ages.append(age)

            if age < stats.youngest_age:
                stats.youngest_age = age
                stats.youngest = user

            if age > stats.oldest_age:
                stats.oldest_age = age
                stats.oldest = user

    stats.avg_age = round(sum(ages) / len(ages), 1) if ages else 0

    # Altersverteilung
    age_groups = {
        "0-17 Jahre": 0,
        "18-25 Jahre": 0,
        "26-35 Jahre": 0,
        "36-50 Jahre": 0,
        "51-65 Jahre": 0,
        "66+ Jahre": 0
    }

    for age in ages:
        if age < 18:
            age_groups["0-17 Jahre"] += 1
        elif age <= 25:
            age_groups["18-25 Jahre"] += 1
        elif age <= 35:
            age_groups["26-35 Jahre"] += 1
        elif age <= 50:
            age_groups["36-50 Jahre"] += 1
        elif age <= 65:
            age_groups["51-65 Jahre"] += 1
        else:
            age_groups["66+ Jahre"] += 1

    stats.age_distribution = age_groups
    stats.max_age_group = max(age_groups.values()) if age_groups.values() else 1

    # Häufigste Namen
    first_names = [p.vorname for p in users if p.vorname]
    last_names = [p.nachname for p in users if p.nachname]

    stats.common_first_names = Counter(first_names).most_common(10)
    stats.common_last_names = Counter(last_names).most_common(10)
    
    # Geburten nach Monaten
    month_names = [
        "Januar", "Februar", "März", "April", "Mai", "Juni",
        "Juli", "August", "September", "Oktober", "November", "Dezember"
    ]
    
    birth_months = Counter()
    for user in users:
        if user.geburtsdatum:
            month_idx = user.geburtsdatum.month - 1
            birth_months[month_names[month_idx]] += 1

    total_births = sum(birth_months.values())
    stats.birth_months = {}
    
    for month in month_names:
        count = birth_months.get(month, 0)
        percentage = round((count / total_births * 100), 1) if total_births > 0 else 0
        stats.birth_months[month] = SimpleNamespace(count=count, percentage=percentage)

    return stats
