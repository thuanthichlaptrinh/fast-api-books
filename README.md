# FastAPI Books API

API quản lý sách, tác giả và danh mục sử dụng FastAPI và SQLAlchemy theo kiến trúc phân tầng (Layered Architecture).

## Tính năng

-   ✅ Quản lý sách (CRUD)
-   ✅ Quản lý tác giả (CRUD)
-   ✅ Quản lý danh mục (CRUD)
-   ✅ Upload ảnh bìa sách
-   ✅ SQLAlchemy ORM
-   ✅ Alembic migrations
-   ✅ Pydantic schemas
-   ✅ Repository Pattern
-   ✅ Service Layer
-   ✅ Dependency Injection

## Kiến trúc dự án

Dự án sử dụng **Layered Architecture** với các tầng rõ ràng:

```
├── app/
│   ├── api/                    # API Layer
│   │   ├── deps.py            # Dependencies (DB session, auth...)
│   │   └── endpoints/         # API endpoints/routes
│   │       ├── authors.py
│   │       ├── books.py
│   │       └── categories.py
│   │
│   ├── services/              # Service Layer (Business Logic)
│   │   ├── author_service.py
│   │   ├── book_service.py
│   │   └── category_service.py
│   │
│   ├── repositories/          # Repository Layer (Data Access)
│   │   ├── base.py           # Base Repository với CRUD chung
│   │   ├── author_repository.py
│   │   ├── book_repository.py
│   │   └── category_repository.py
│   │
│   ├── models/                # Database Models (ORM)
│   │   ├── author.py
│   │   ├── book.py
│   │   └── category.py
│   │
│   ├── schemas/               # Pydantic Schemas (Validation)
│   │   ├── author.py
│   │   ├── book.py
│   │   └── category.py
│   │
│   ├── core/                  # Core configurations
│   │   └── config.py
│   │
│   ├── db/                    # Database configuration
│   │   ├── base.py
│   │   └── session.py
│   │
│   ├── static/                # Static files
│   │   └── covers/           # Book cover images
│   │
│   └── main.py               # Application entry point
│
├── migration/                 # Alembic migrations
├── .env.example              # Environment variables template
├── requirements.txt          # Python dependencies
└── README.md
```

## Các tầng trong kiến trúc

### 1. **API Layer** (`app/api/endpoints/`)

-   Xử lý HTTP requests/responses
-   Validation input từ client
-   Gọi Service Layer để xử lý business logic
-   Không chứa business logic

### 2. **Service Layer** (`app/services/`)

-   Chứa toàn bộ business logic
-   Xử lý validation nghiệp vụ
-   Gọi Repository Layer để tương tác với database
-   Xử lý exceptions và error handling

### 3. **Repository Layer** (`app/repositories/`)

-   Truy vấn và thao tác với database
-   Cung cấp interface trừu tượng cho data access
-   Không chứa business logic
-   Sử dụng Base Repository Pattern

### 4. **Models Layer** (`app/models/`)

-   Định nghĩa database schema (SQLAlchemy ORM)
-   Relationships giữa các entities

### 5. **Schemas Layer** (`app/schemas/`)

-   Validation và serialization dữ liệu (Pydantic)
-   Request/Response models

## Cài đặt

### 1. Clone repository

```bash
git clone <repository-url>
cd fast-api-books
```

### 2. Tạo môi trường ảo

```bash
python -m venv venv
```

### 3. Kích hoạt môi trường ảo

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

### 4. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 5. Tạo file .env

```bash
cp .env.example .env
```

Chỉnh sửa file `.env` theo cấu hình của bạn.

### 6. Chạy migration

```bash
alembic upgrade head
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

API sẽ chạy tại: `http://localhost:8000`

## API Documentation

Sau khi chạy server, truy cập:

-   **Swagger UI**: `http://localhost:8000/docs`
-   **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Books

-   `GET /api/books/` - Lấy danh sách sách (pagination)
-   `GET /api/books/{id}` - Lấy thông tin sách theo ID
-   `GET /api/books/author/{author_id}` - Lấy sách theo tác giả
-   `GET /api/books/category/{category_id}` - Lấy sách theo danh mục
-   `GET /api/books/search/?keyword=...` - Tìm kiếm sách theo tên
-   `POST /api/books/` - Tạo sách mới
-   `PUT /api/books/{id}` - Cập nhật sách
-   `DELETE /api/books/{id}` - Xóa sách

### Authors

-   `GET /api/authors/` - Lấy danh sách tác giả (pagination)
-   `GET /api/authors/{id}` - Lấy thông tin tác giả theo ID
-   `GET /api/authors/search/?keyword=...` - Tìm kiếm tác giả theo tên
-   `POST /api/authors/` - Tạo tác giả mới
-   `PUT /api/authors/{id}` - Cập nhật tác giả
-   `DELETE /api/authors/{id}` - Xóa tác giả

### Categories

-   `GET /api/categories/` - Lấy danh sách danh mục (pagination)
-   `GET /api/categories/{id}` - Lấy thông tin danh mục theo ID
-   `GET /api/categories/search/?keyword=...` - Tìm kiếm danh mục theo tên
-   `POST /api/categories/` - Tạo danh mục mới
-   `PUT /api/categories/{id}` - Cập nhật danh mục
-   `DELETE /api/categories/{id}` - Xóa danh mục

## Database Migration (Alembic)

### Khởi tạo Alembic (nếu chưa có)

```bash
alembic init migration
```

### Tạo migration mới

```bash
alembic revision --autogenerate -m "init tables"
```

### Chạy migration

```bash
alembic upgrade head
```

### Xem lịch sử migration

```bash
alembic history
```

### Rollback migration

```bash
alembic downgrade -1
```

## Workflow Development

### 1. Tạo một feature mới

#### Bước 1: Tạo Model (Database Schema)

```python
# app/models/new_model.py
class NewModel(Base):
    __tablename__ = "new_models"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
```

#### Bước 2: Tạo Schema (Validation)

```python
# app/schemas/new_model.py
class NewModelBase(BaseModel):
    name: str

class NewModelCreate(NewModelBase):
    pass

class NewModel(NewModelBase):
    id: int
    class Config:
        from_attributes = True
```

#### Bước 3: Tạo Repository (Data Access)

```python
# app/repositories/new_model_repository.py
from app.repositories.base import BaseRepository

class NewModelRepository(BaseRepository[NewModel]):
    def __init__(self):
        super().__init__(NewModel)
```

#### Bước 4: Tạo Service (Business Logic)

```python
# app/services/new_model_service.py
class NewModelService:
    def __init__(self):
        self.repository = new_model_repository

    def create_item(self, db: Session, item_in):
        # Business logic here
        return self.repository.create(db, item_in.model_dump())
```

#### Bước 5: Tạo Endpoint (API)

```python
# app/api/endpoints/new_models.py
@router.post("/", response_model=NewModel)
def create_item(item: NewModelCreate, db: Session = Depends(get_db)):
    return new_model_service.create_item(db, item)
```

## Technologies

-   **FastAPI** - Modern, fast web framework
-   **SQLAlchemy** - SQL toolkit and ORM
-   **Alembic** - Database migration tool
-   **Pydantic** - Data validation using Python type hints
-   **Uvicorn** - ASGI server implementation
-   **Python-multipart** - File upload support

## Best Practices

1. **Separation of Concerns**: Mỗi tầng có trách nhiệm riêng biệt
2. **Dependency Injection**: Sử dụng FastAPI Depends
3. **Repository Pattern**: Trừu tượng hóa data access
4. **Service Layer**: Tập trung business logic
5. **Type Hints**: Sử dụng Python type hints toàn bộ code
6. **Error Handling**: Xử lý lỗi tập trung tại Service Layer
7. **Validation**: Pydantic schemas cho input/output validation

## License

MIT
