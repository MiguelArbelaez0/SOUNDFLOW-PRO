from database import supabase

try:
    respuesta = supabase.table("canciones_vectoriales").select("*").execute()
    print("¡Puente establecido!")
    print("Datos encontrados:", respuesta.data)

except Exception as e:
    print("Error al conectar con Supabase:")
    print(e)