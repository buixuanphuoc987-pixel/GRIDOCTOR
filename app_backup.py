import os
import pickle
import tempfile

import faiss
import streamlit as st
from sentence_transformers import SentenceTransformer
from ultralytics import YOLO


# =========================================================
# 1. CẤU HÌNH HỆ THỐNG
# =========================================================

MODEL_PATH = "runs/classify/runs/melon_classifier/weights/best.pt"
VECTOR_FOLDER = "vector_db"

CONFIDENCE_THRESHOLD = 0.70

CLASS_NAMES_VI = {
    "Healthy": "Cây dưa khỏe mạnh",
    "Downy Mildew": "Bệnh sương mai",
    "Downy_Mildew": "Bệnh sương mai",
    "Powdery Mildew": "Bệnh phấn trắng",
    "Powdery_Mildew": "Bệnh phấn trắng",
    "Thrips": "Bọ trĩ",
}


# =========================================================
# 2. CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="GRIDOCTOR",
    page_icon="🌱",
    layout="centered"
)


# =========================================================
# 3. GIAO DIỆN CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .sub-title {
        text-align: center;
        font-size: 18px;
        color: #555555;
        margin-bottom: 25px;
    }

    .result-box {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #dddddd;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .footer {
        text-align: center;
        color: #777777;
        font-size: 13px;
        margin-top: 40px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 4. TIÊU ĐỀ
# =========================================================

st.markdown(
    '<div class="main-title">🌱 GRIDOCTOR</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Trợ lý AI nhận diện và tư vấn bệnh, sâu hại trên cây dưa lưới'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# 5. GIỚI THIỆU
# =========================================================

with st.expander("📖 Giới thiệu hệ thống"):

    st.markdown(
        """
        **GRIDOCTOR** kết hợp:

        - Mô hình **YOLO Classification** để nhận diện hình ảnh.
        - **Sentence Transformers** để tạo vector ngữ nghĩa.
        - **FAISS** để truy xuất tài liệu.
        - Hệ thống **RAG** để cung cấp kiến thức phù hợp.

        Hệ thống hiện hỗ trợ:

        - 🌿 Cây dưa khỏe mạnh
        - 🌧️ Bệnh sương mai
        - ⚪ Bệnh phấn trắng
        - 🐛 Bọ trĩ
        """
    )


with st.expander("📌 Hướng dẫn sử dụng"):

    st.markdown(
        """
        **Bước 1:** Chọn một ảnh lá dưa rõ nét.

        **Bước 2:** Bấm nút **NHẬN DIỆN**.

        **Bước 3:** Xem tên bệnh và độ tin cậy.

        **Bước 4:** Nếu độ tin cậy từ **70% trở lên**, hệ thống sẽ cung cấp tư vấn RAG.

        **Bước 5:** Nếu dưới **70%**, hãy chụp lại ảnh rõ hơn.
        """
    )

st.divider()


# =========================================================
# 6. TẢI MÔ HÌNH YOLO
# =========================================================

@st.cache_resource
def load_yolo():

    model = YOLO(MODEL_PATH)

    return model


# =========================================================
# 7. TẢI HỆ THỐNG RAG
# =========================================================

@st.cache_resource
def load_rag():

    embedding_model = SentenceTransformer(
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    index = faiss.read_index(
        os.path.join(
            VECTOR_FOLDER,
            "knowledge.index"
        )
    )

    with open(
        os.path.join(
            VECTOR_FOLDER,
            "documents.pkl"
        ),
        "rb"
    ) as file:

        data = pickle.load(file)

    return embedding_model, index, data


# =========================================================
# 8. HÀM TÁCH TÀI LIỆU
# =========================================================

def tach_noi_dung(text):

    sections = {
        "MÔ TẢ": "",
        "TRIỆU CHỨNG": "",
        "DẤU HIỆU NHẬN BIẾT": "",
        "NGUYÊN NHÂN": "",
        "ĐIỀU KIỆN PHÁT SINH": "",
        "PHÒNG NGỪA": "",
        "KHUYẾN NGHỊ CHĂM SÓC": "",
        "XỬ LÝ": "",
        "LƯU Ý": ""
    }

    current_section = None

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        title = line.rstrip(":").strip()

        if title in sections:

            current_section = title

            continue

        if current_section:

            sections[current_section] += line + "\n"

    return sections


# =========================================================
# 9. KHỞI TẠO MÔ HÌNH
# =========================================================

yolo_model = load_yolo()

embedding_model, index, data = load_rag()

documents = data["documents"]

metadata = data["metadata"]


# =========================================================
# 10. CHỌN ẢNH
# =========================================================

st.subheader("📷 Chọn ảnh cần kiểm tra")

uploaded_file = st.file_uploader(
    "Tải ảnh lá dưa lên hệ thống",
    type=[
        "jpg",
        "jpeg",
        "png"
    ]
)


# =========================================================
# 11. XỬ LÝ ẢNH
# =========================================================

if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="Ảnh đã chọn",
        use_container_width=True
    )

    st.write("")

    if st.button(
        "🔍 NHẬN DIỆN",
        use_container_width=True
    ):

        suffix = os.path.splitext(
            uploaded_file.name
        )[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(
                uploaded_file.getbuffer()
            )

            image_path = temp_file.name


        try:

            # =================================================
            # 12. YOLO DỰ ĐOÁN
            # =================================================

            with st.spinner(
                "Đang phân tích ảnh..."
            ):

                results = yolo_model.predict(
                    source=image_path,
                    verbose=False
                )


            result = results[0]

            class_id = result.probs.top1

            class_name = result.names[
                class_id
            ]

            confidence = (
                result.probs.top1conf.item()
            )


            display_name = CLASS_NAMES_VI.get(
                class_name,
                class_name
            )


            # =================================================
            # 13. HIỂN THỊ KẾT QUẢ
            # =================================================

            st.success(
                "✅ Đã hoàn thành nhận diện"
            )

            st.subheader(
                "🔍 KẾT QUẢ NHẬN DIỆN"
            )


            col1, col2 = st.columns(2)


            with col1:

                st.metric(
                    label="Kết quả",
                    value=display_name
                )


            with col2:

                st.metric(
                    label="Độ tin cậy",
                    value=f"{confidence * 100:.2f}%"
                )


            # =================================================
            # 14. KẾT QUẢ ĐỘ TIN CẬY THẤP
            # =================================================

            if confidence < CONFIDENCE_THRESHOLD:

                st.warning(
                    "⚠️ Kết quả nhận diện chưa đủ tin cậy."
                )

                st.info(
                    "Hãy chụp lại ảnh rõ hơn, đủ ánh sáng, "
                    "chụp gần vùng lá có triệu chứng và "
                    "hạn chế nền ảnh phức tạp."
                )

                st.error(
                    "Hệ thống chưa đưa ra tư vấn xử lý "
                    "vì độ tin cậy chưa đạt 70%."
                )


            # =================================================
            # 15. RAG
            # =================================================

            else:

                with st.spinner(
                    "Đang truy xuất kho kiến thức..."
                ):

                    query = (
                        f"Thông tin về {class_name} "
                        f"trên cây dưa lưới"
                    )


                    question_vector = (
                        embedding_model.encode(
                            [query],
                            convert_to_numpy=True,
                            normalize_embeddings=True
                        )
                    )


                    scores, indices = (
                        index.search(
                            question_vector,
                            k=1
                        )
                    )


                    best_index = int(
                        indices[0][0]
                    )


                    best_score = float(
                        scores[0][0]
                    )


                    retrieved_text = (
                        documents[
                            best_index
                        ]
                    )


                # =================================================
                # 16. THÔNG TIN RAG
                # =================================================

                st.divider()

                st.subheader(
                    "📚 TƯ VẤN TỪ HỆ THỐNG RAG"
                )


                with st.expander(
                    "🔎 Thông tin truy xuất"
                ):

                    st.write(
                        "**Nguồn tài liệu:**",
                        metadata[
                            best_index
                        ]
                    )

                    st.write(
                        "**Độ tương đồng:**",
                        round(
                            best_score,
                            4
                        )
                    )


                sections = tach_noi_dung(
                    retrieved_text
                )


                # =================================================
                # 17. HIỂN THỊ TỪNG PHẦN
                # =================================================

                if sections["MÔ TẢ"]:

                    st.subheader(
                        "📋 MÔ TẢ"
                    )

                    st.write(
                        sections[
                            "MÔ TẢ"
                        ]
                    )


                if sections["TRIỆU CHỨNG"]:

                    st.subheader(
                        "🔎 TRIỆU CHỨNG"
                    )

                    st.write(
                        sections[
                            "TRIỆU CHỨNG"
                        ]
                    )


                if sections[
                    "DẤU HIỆU NHẬN BIẾT"
                ]:

                    st.subheader(
                        "👁️ DẤU HIỆU NHẬN BIẾT"
                    )

                    st.write(
                        sections[
                            "DẤU HIỆU NHẬN BIẾT"
                        ]
                    )


                if sections["NGUYÊN NHÂN"]:

                    st.subheader(
                        "🦠 NGUYÊN NHÂN"
                    )

                    st.write(
                        sections[
                            "NGUYÊN NHÂN"
                        ]
                    )


                if sections[
                    "ĐIỀU KIỆN PHÁT SINH"
                ]:

                    st.subheader(
                        "🌦️ ĐIỀU KIỆN PHÁT SINH"
                    )

                    st.write(
                        sections[
                            "ĐIỀU KIỆN PHÁT SINH"
                        ]
                    )


                if sections["PHÒNG NGỪA"]:

                    st.subheader(
                        "🛡️ PHÒNG NGỪA"
                    )

                    st.write(
                        sections[
                            "PHÒNG NGỪA"
                        ]
                    )


                if sections[
                    "KHUYẾN NGHỊ CHĂM SÓC"
                ]:

                    st.subheader(
                        "🌿 KHUYẾN NGHỊ CHĂM SÓC"
                    )

                    st.write(
                        sections[
                            "KHUYẾN NGHỊ CHĂM SÓC"
                        ]
                    )


                if sections["XỬ LÝ"]:

                    st.subheader(
                        "💊 XỬ LÝ"
                    )

                    st.write(
                        sections[
                            "XỬ LÝ"
                        ]
                    )


                if sections["LƯU Ý"]:

                    st.warning(
                        "⚠️ LƯU Ý"
                    )

                    st.write(
                        sections[
                            "LƯU Ý"
                        ]
                    )


                # =================================================
                # 18. CẢNH BÁO CHUNG
                # =================================================

                st.divider()

                st.caption(
                    "⚠️ GRIDOCTOR là hệ thống hỗ trợ. "
                    "Kết quả không thay thế hoàn toàn "
                    "ý kiến của chuyên gia nông nghiệp."
                )


        # =====================================================
        # 19. XỬ LÝ LỖI
        # =====================================================

        except Exception as error:

            st.error(
                "Có lỗi xảy ra trong quá trình xử lý."
            )

            st.exception(error)


        # =====================================================
        # 20. XÓA FILE TẠM
        # =====================================================

        finally:

            if os.path.exists(
                image_path
            ):

                os.remove(
                    image_path
                )


# =========================================================
# 21. CHÂN TRANG
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        🌱 GRIDOCTOR - Hệ thống AI hỗ trợ nhận diện
        bệnh và sâu hại trên cây dưa lưới
    </div>
    """,
    unsafe_allow_html=True
)