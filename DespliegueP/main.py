from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Tarea(BaseModel):
    id: int = None
    titulo: str
    descripcion: str
    completada: bool = False

tareas: List[Tarea] = []

@app.get("/")
async def serve_index():
    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    return FileResponse(html_path)

@app.get("/tareas")
async def listar_tareas():
    return tareas

@app.post("/tareas")
async def crear_tarea(tarea: Tarea):
    tarea.id = len(tareas) + 1
    tareas.append(tarea)
    return {"mensaje": "Tarea creada exitosamente", "tarea": tarea}

@app.delete("/tareas/{id}")
async def eliminar_tarea(id: int):
    global tareas
    tarea_encontrada = next((t for t in tareas if t.id == id), None)
    if not tarea_encontrada:
        return {"error": "Tarea no encontrada"}
    tareas = [t for t in tareas if t.id != id]
    return {"mensaje": "Tarea eliminada", "tarea": tarea_encontrada}

@app.put("/tareas/{id}")
async def actualizar_tarea(id: int, tarea_actualizada: Tarea):
    tarea_encontrada = next((t for t in tareas if t.id == id), None)
    if not tarea_encontrada:
        return {"error": "Tarea no encontrada"}
    tarea_actualizada.id = id
    index = tareas.index(tarea_encontrada)
    tareas[index] = tarea_actualizada
    return {"mensaje": "Tarea actualizada", "tarea": tarea_actualizada}