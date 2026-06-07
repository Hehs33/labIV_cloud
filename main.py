from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os


app = FastAPI(title="API Distribuida - Laboratorio IV")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Tarea(BaseModel):
    id: Optional[int] = None
    titulo: str
    descripcion: str
    completada: bool = False

tareas: List[Tarea] = []
contador_id = 0

@app.get("/")
def serve_index():
    html_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "index.html")
    return FileResponse(html_path)

@app.get("/tareas")
def listar_tareas():
    return tareas

@app.post("/tareas", status_code=status.HTTP_201_CREATED)
def crear_tarea(tarea: Tarea):
    global contador_id
    contador_id += 1
    tarea.id = contador_id
    tareas.append(tarea)
    return {"mensaje": "Tarea creada exitosamente", "tarea": tarea}

@app.delete("/tareas/{id}", status_code=status.HTTP_200_OK)
def eliminar_tarea(id: int):
    tarea_encontrada = next((t for t in tareas if t.id == id), None)
    if not tarea_encontrada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    tareas.remove(tarea_encontrada)
    return {"mensaje": "Tarea eliminada", "tarea": tarea_encontrada}

@app.put("/tareas/{id}", status_code=status.HTTP_200_OK)
def actualizar_tarea(id: int, tarea_actualizada: Tarea):
    tarea_encontrada = next((t for t in tareas if t.id == id), None)
    if not tarea_encontrada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    tarea_actualizada.id = id
    index = tareas.index(tarea_encontrada)
    tareas[index] = tarea_actualizada
    return {"mensaje": "Tarea actualizada", "tarea": tarea_actualizada}
