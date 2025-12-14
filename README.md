# FastAPI Books API

API quản lý sách, tác giả và danh mục sử dụng FastAPI và SQLAlchemy.

## Tính năng

-   ✅ Quản lý sách (CRUD)
-   ✅ Quản lý tác giả (CRUD)
-   ✅ Quản lý danh mục (CRUD)
-   ✅ Upload ảnh bìa sách
-   ✅ SQLAlchemy ORM
-   ✅ Alembic migrations
-   ✅ Pydantic schemas

## Cấu trúc dự án

```
app/
├── api/
│   ├── deps.py           # Dependencies
│   └── endpoints/        # API endpoints
│       ├── authors.py
│       ├── books.py
│       └── categories.py
├── core/
│   └── config.py         # Configuration
├── db/
│   ├── base.py          # Database models base
│   └── session.py       # Database session
├── models/              # SQLAlchemy models
│   ├── author.py
│   ├── book.py
│   └── category.py
├── schemas/             # Pydantic schemas
│   ├── author.py
│   ├── book.py
│   └── category.py
└── static/
    └── covers/          # Book cover images
```

## Cài đặt

### 1. Tạo môi trường ảo

```bash
python -m venv .venv
```

### 2. Kích hoạt môi trường ảo

**Windows:**

```bash
.venv\Scripts\activate
```

**Linux/Mac:**

```bash
source .venv/bin/activate
```

### 3. Cài đặt dependencies

```bash
pip install "fastapi[standard]" sqlalchemy alembic python-multipart
```

## Chạy ứng dụng

### Cách 1: Sử dụng FastAPI CLI (Khuyến nghị)

**Development mode (với auto-reload):**

```bash
fastapi dev app/main.py
```

**Production mode:**

```bash
fastapi run app/main.py
```

### Cách 2: Sử dụng Uvicorn trực tiếp

**Development mode (với auto-reload):**

```bash
uvicorn app.main:app --reload
```

**Production mode:**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Chạy với port tùy chỉnh:**

```bash
uvicorn app.main:app --reload --port 8080
```

API sẽ chạy tại: `http://localhost:8000` (hoặc port bạn chỉ định)

## API Documentation

Sau khi chạy server, truy cập:

-   Swagger UI: `http://localhost:8000/docs`
-   ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Books

-   `GET /api/books/` - Lấy danh sách sách
-   `GET /api/books/{id}` - Lấy thông tin sách
-   `POST /api/books/` - Tạo sách mới
-   `PUT /api/books/{id}` - Cập nhật sách
-   `DELETE /api/books/{id}` - Xóa sách

### Authors

-   `GET /api/authors/` - Lấy danh sách tác giả
-   `GET /api/authors/{id}` - Lấy thông tin tác giả
-   `POST /api/authors/` - Tạo tác giả mới
-   `PUT /api/authors/{id}` - Cập nhật tác giả
-   `DELETE /api/authors/{id}` - Xóa tác giả

### Categories

-   `GET /api/categories/` - Lấy danh sách danh mục
-   `GET /api/categories/{id}` - Lấy thông tin danh mục
-   `POST /api/categories/` - Tạo danh mục mới
-   `PUT /api/categories/{id}` - Cập nhật danh mục
-   `DELETE /api/categories/{id}` - Xóa danh mục

## Database Migration (Alembic)

### Khởi tạo Alembic (nếu chưa có)

```bash
alembic init alembic
```

### Tạo migration mới

```bash
alembic revision --autogenerate -m "migration message"
```

### Chạy migration

```bash
alembic upgrade head
```

### Rollback migration

```bash
alembic downgrade -1
```

## Technologies

-   **FastAPI** - Modern web framework
-   **SQLAlchemy** - SQL toolkit and ORM
-   **Alembic** - Database migration tool
-   **Pydantic** - Data validation
-   **Python-multipart** - File upload support

## License

MIT
