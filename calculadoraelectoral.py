import streamlit as st

def calcular_bancas(porcentajes_fuerzas, total_bancas):
    suma_principales = sum(porcentajes_fuerzas)
    porcentaje_restante = 100 - suma_principales

    # Cuociente electoral en porcentaje
    cuociente_electoral = 100 / total_bancas

    bancas_por_cociente = []
    residuos = []
    for porcentaje in porcentajes_fuerzas:
        if porcentaje >= cuociente_electoral:
            bancas = int(porcentaje // cuociente_electoral)
            residuo = porcentaje % cuociente_electoral
        else:
            bancas = 0
            residuo = -1
        bancas_por_cociente.append(bancas)
        residuos.append(residuo)

    bancas_asignadas = sum(bancas_por_cociente)
    bancas_restantes = total_bancas - bancas_asignadas

    while bancas_restantes > 0:
        max_residuo = max(residuos)
        if max_residuo <= -1:
            break
        max_idx = residuos.index(max_residuo)
        bancas_por_cociente[max_idx] += 1
        residuos[max_idx] = -1
        bancas_restantes -= 1

    if bancas_restantes > 0:
        max_votos_idx = porcentajes_fuerzas.index(max(porcentajes_fuerzas))
        bancas_por_cociente[max_votos_idx] += bancas_restantes

    return bancas_por_cociente, porcentaje_restante

# Streamlit App
st.title("🗳️ Calculadora de bancas legislativas - PBA - https://x.com/iterAR_eco")

st.write("Ingresá los porcentajes de votos de las fuerzas que superarán el piso electoral y la cantidad de bancas en juego para cada categoría.")

num_fuerzas = st.number_input("¿Cuántas fuerzas querés cargar?", min_value=2, max_value=10, value=3)

porcentajes_fuerzas = []
for i in range(num_fuerzas):
    porcentaje = st.number_input(f"Porcentaje de votos de la fuerza {i+1} (%)", min_value=0.0, max_value=100.0, step=0.1)
    porcentajes_fuerzas.append(porcentaje)

suma_porcentajes = sum(porcentajes_fuerzas)
if suma_porcentajes > 100:
    st.error(f"La suma de los porcentajes ({suma_porcentajes:.2f}%) supera el 100%. Corregilo para continuar.")
else:
    st.subheader("⚙️ Bancas en juego por categoría")
    bancas_concejales = st.number_input("Cantidad de bancas a repartir (Concejales)", min_value=1, value=12)
    bancas_diputados = st.number_input("Cantidad de bancas a repartir (Diputados)", min_value=1, value=6)

    if st.button("Calcular bancas"):
        # Concejales
        bancas_c, restante_c = calcular_bancas(porcentajes_fuerzas, bancas_concejales)
        st.subheader(f"🔹 Concejales ({bancas_concejales} bancas en juego)")
        for idx, (p, b) in enumerate(zip(porcentajes_fuerzas, bancas_c), 1):
            st.write(f"Fuerza {idx}: {p:.2f}% votos - {b} bancas")
        st.write(f"Porcentaje de otras fuerzas sin bancas: {restante_c:.2f}%")

        # Diputados
        bancas_d, restante_d = calcular_bancas(porcentajes_fuerzas, bancas_diputados)
        st.subheader(f"🔹 Diputados ({bancas_diputados} bancas en juego)")
        for idx, (p, b) in enumerate(zip(porcentajes_fuerzas, bancas_d), 1):
            st.write(f"Fuerza {idx}: {p:.2f}% votos - {b} bancas")
        st.write(f"Porcentaje de otras fuerzas sin bancas: {restante_d:.2f}%")
