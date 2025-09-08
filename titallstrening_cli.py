#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Titallstrening – CLI
Øv på å gange og dele med 10, 100 og 1000.
Viser desimaltall med komma, og godtar både komma og punktum i svar.
"""

import random
from decimal import Decimal, getcontext

getcontext().prec = 28

FACTORS = [Decimal(10), Decimal(100), Decimal(1000)]

def fmt(n: Decimal) -> str:
    """Format with comma as decimal separator; strip trailing zeros."""
    s = format(n, 'f').rstrip('0').rstrip('.')
    s = s.replace('.', ',')
    if s == '':  # if n was 0.0
        s = '0'
    return s

def parse_user(s: str) -> Decimal:
    s = s.strip().replace(' ', '').replace(',', '.')
    return Decimal(s)

def random_number(difficulty: str) -> Decimal:
    """
    difficulty: 'hel', 'desimal', 'blandet'
    """
    if difficulty == 'hel':
        # Integers up to 4 digits incl. some with trailing zeros
        choices = [random.randint(1, 9999), random.choice([10,20,30,40,50,60,70,80,90,100,200,500,1000])]
        n = Decimal(random.choice(choices))
    elif difficulty == 'desimal':
        # Decimals with 1–3 decimals, range roughly 0.01–999.9
        whole = random.randint(0, 999)
        frac_places = random.choice([1,2,3])
        frac = random.randint(1, 9*(10**(frac_places-1)))
        n = Decimal(f"{whole}.{str(frac).zfill(frac_places)}")
    else:
        # blandet
        return random_number(random.choice(['hel','desimal']))
    # Occasionally make it small (<1)
    if random.random() < 0.2:
        frac_places = random.choice([1,2,3])
        frac = random.randint(1, 9*(10**(frac_places-1)))
        n = Decimal(f"0.{str(frac).zfill(frac_places)}")
    return n

def make_task(ops: list[str], allowed_factors: list[Decimal], difficulty: str):
    a = random_number(difficulty)
    op = random.choice(ops)  # '*' or '/'
    f = random.choice(allowed_factors)
    if op == '*':
        correct = a * f
        return f"{fmt(a)} · {fmt(f)} = ?", correct
    else:
        correct = a / f
        return f"{fmt(a)} : {fmt(f)} = ?", correct

def menu_choice(prompt: str, options: dict):
    while True:
        print(prompt)
        for k, v in options.items():
            print(f"  {k}) {v}")
        choice = input("> ").strip().lower()
        if choice in options:
            return choice
        print("Ugyldig valg, prøv igjen.\n")

def main():
    print("=== Titallstrening (CLI) ===")
    # Velg operasjoner
    op_choice = menu_choice("Velg operasjon(er):", {
        '1': 'Gange (·)',
        '2': 'Dele (:)',
        '3': 'Begge'
    })
    if op_choice == '1':
        ops = ['*']
    elif op_choice == '2':
        ops = ['/']
    else:
        ops = ['*','/']

    # Velg faktorer
    fac_choice = menu_choice("Tillatte faktorer:", {
        '1': '10',
        '2': '100',
        '3': '1000',
        '4': 'Alle (10, 100, 1000)'
    })
    if fac_choice == '1':
        allowed = [Decimal(10)]
    elif fac_choice == '2':
        allowed = [Decimal(100)]
    elif fac_choice == '3':
        allowed = [Decimal(1000)]
    else:
        allowed = FACTORS

    # Vanskelighetsgrad
    diff_choice = menu_choice("Talltype:", {
        '1': 'Hele tall',
        '2': 'Desimaltall',
        '3': 'Blandet'
    })
    diff_map = {'1':'hel', '2':'desimal', '3':'blandet'}
    difficulty = diff_map[diff_choice]

    # Antall oppgaver
    while True:
        try:
            n = int(input("Hvor mange oppgaver? (f.eks. 20): ").strip())
            if 1 <= n <= 999:
                break
            print("Skriv et tall mellom 1 og 999.")
        except:
            print("Skriv et heltall.")

    print("\nSkriv svar med enten komma eller punktum. Trykk Enter for å hoppe over.\n")

    correct = 0
    attempted = 0
    for i in range(1, n+1):
        task, ans = make_task(ops, allowed, difficulty)
        print(f"Oppgave {i}: {task}")
        user = input("Svar: ").strip()
        if user == "":
            print(f"   Løsning: {fmt(ans)}\n")
            continue
        try:
            u = parse_user(user)
            attempted += 1
            if u == ans:
                print("   Riktig! ✅\n")
                correct += 1
            else:
                print(f"   Feil. Riktig svar er {fmt(ans)}.\n")
        except Exception as e:
            print(f"   Kunne ikke tolke svaret. Riktig svar er {fmt(ans)}.\n")

    print("=== Resultat ===")
    print(f"Riktige: {correct} av {attempted} (forsøkt {attempted} / totalt {n})")
    if attempted:
        pct = 100*correct/attempted
        print(f"Treffsikkerhet: {pct:.0f}%")
    print("Bra jobba!")

if __name__ == "__main__":
    main()
