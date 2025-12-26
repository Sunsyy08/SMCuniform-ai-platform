from fastapitest.database import get_db_connection

# 벌점 정책 (나중에 바꿀 수 있음)
VIOLATION_POINTS = 5

def handle_detection(student_number: str, name: str, uniform_detected: bool):
    conn = get_db_connection()
    if conn is None:
        print("❌ DB 연결 실패")
        return

    try:
        with conn.cursor() as cursor:

            # 1️⃣ detections 기록
            detected_result = "교복 착용" if uniform_detected else "교복 미착용"
            is_violation = not uniform_detected

            cursor.execute(
                """
                INSERT INTO detections
                (student_number, name, detected_result, is_violation)
                VALUES (%s, %s, %s, %s)
                """,
                (student_number, name, detected_result, is_violation)
            )

            detection_id = cursor.lastrowid

            # 2️⃣ 교복 미착용 → 벌점 + 알림
            if is_violation:
                # 벌점
                cursor.execute(
                    """
                    INSERT INTO penalties
                    (student_number, name, points, reason, detection_id)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        student_number,
                        name,
                        VIOLATION_POINTS,
                        "교복 미착용",
                        detection_id
                    )
                )

                # 알림
                cursor.execute(
                    """
                    INSERT INTO alerts
                    (student_number, name, title, message, penalty_points, detection_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        student_number,
                        name,
                        "복장 규정 위반",
                        "교복 미착용이 감지되었습니다.",
                        VIOLATION_POINTS,
                        detection_id
                    )
                )

        conn.commit()
        print("✅ 감지 기록 DB 저장 완료")

    except Exception as e:
        conn.rollback()
        print("❌ DB 저장 오류:", e)

    finally:
        conn.close()
