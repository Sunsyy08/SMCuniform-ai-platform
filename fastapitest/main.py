from fastapi import FastAPI, UploadFile, File, Form
from fastapitest.database import get_db_connection
from fastapitest.image_utils import save_image
from fastapitest.ai_service import detect_uniform
from fastapitest.detection_service import handle_detection
from contextlib import asynccontextmanager
from fastapitest.ai_service import load_model
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Server started")
    get_db_connection()
    load_model()  # 🔥 서버 시작 시 모델 1회 로드
    yield
    print("🛑 Server stopped")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "running"}

@app.get("/students")
def get_students():
    conn = get_db_connection()
    if conn is None:
        return {"error": "DB connection failed"}

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT student_number, name, created_at FROM students"
            )
            return cursor.fetchall()
    finally:
        conn.close()

@app.post("/detect")
async def detect(
    student_number: str = Form(...),
    name: str = Form(...),
    image: UploadFile = File(...)
):
    image_path = save_image(image)
    uniform_detected = detect_uniform(image_path)
    handle_detection(student_number, name, uniform_detected)

    return {
        "student_number": student_number,
        "name": name,
        "uniform_detected": uniform_detected,
        "result": "교복 착용" if uniform_detected else "교복 미착용"
    }

@app.get("/detections")
def get_detections():
    conn = get_db_connection()
    if conn is None:
        return {"error": "DB connection failed"}

    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    DATE(detected_at) AS date,
                    TIME(detected_at) AS time,
                    student_number,
                    name,
                    detected_result,
                    is_violation
                FROM detections
                ORDER BY detected_at DESC
            """)
            return cursor.fetchall()
    finally:
        conn.close()
