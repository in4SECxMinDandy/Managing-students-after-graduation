# Module Core

## Base Classes dùng chung

### BaseModel

Location: `app/Modules/Core/BaseModel.php`

Các tính năng:
- Kế thừa `Illuminate\Database\Eloquent\Model`
- Đã thêm `SoftDeletes` trait
- Mặc định `primaryKey`, `incrementing`, `keyType` có thể override

Tất cả Models trong hệ thống kế thừa `BaseModel` thay vì Model trực tiếp.

### BaseService

Location: `app/Modules/Core/BaseService.php`

Các tính năng:
- Static property `$model` chỉ định model class
- Constructor auto-resolve model qua `$model`
- Các method cơ bản: `all()`, `find()`, `create()`, `update()`, `delete()`, `paginate()`
- Các Service cụ thể kế thừa và extend thêm logic nghiệp vụ

### BaseLivewire

Location: `app/Modules/Core/BaseLivewire.php`

Các tính năng:
- `$layout`: Blade layout mặc định
- `$pageTitle`: Tiêu đề trang
- Helper methods: `success()`, `error()`
- Tất cả Livewire components kế thừa BaseLivewire

### CoreServiceProvider

Location: `app/Modules/Core/CoreServiceProvider.php`

- Load migrations tự động từ `app/Modules/*/Database/Migrations`
- Nơi đăng ký các service bindings nếu cần

## Auth Guards

3 middleware trong `app/Http/Middleware/`:

| Middleware | Guard | Redirect |
|------------|-------|---------|
| `AuthenticateCandidate` | `candidate` | `/candidate/login` |
| `AuthenticateStudent` | `student` | `/student/login` |
| `AuthenticateAdmin` | `admin` | `/admin/login` |

## Config Files

| File | Mục đích |
|------|---------|
| `config/auth.php` | 3 guards + 3 providers |
| `config/sanctum.php` | Sanctum stateful domains |
| `config/livewire.php` | Livewire settings |
| `config/database.php` | MySQL connection |
| `config/app.php` | App name, locale, timezone |
