<?php

namespace App\Modules\SinhVien\Models;

use App\Modules\Core\BaseModel;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Laravel\Sanctum\HasApiTokens;

class SinhVien extends Authenticatable
{
    use HasApiTokens;

    protected $table = 'sinh_vien';

    protected $primaryKey = 'MaSV';

    public $incrementing = false;

    protected $keyType = 'string';

    public $timestamps = false;

    protected $fillable = ['MaSV', 'HoTen', 'NgaySinh', 'Email', 'MatKhau', 'MaLop', 'MaHSO'];

    protected $hidden = ['MatKhau'];

    protected $casts = [
        'HoTen'    => 'string',
        'NgaySinh' => 'date',
        'Email'    => 'string',
        'MatKhau'  => 'string',
    ];

    public function getAuthPassword(): string
    {
        return $this->MatKhau;
    }

    public function lop(): BelongsTo
    {
        return $this->belongsTo(\App\Modules\Lop\Models\Lop::class, 'MaLop', 'MaLop');
    }

    public function hsoXetTuyen(): BelongsTo
    {
        return $this->belongsTo(\App\Modules\TuyenSinh\Models\HSOXetTuyen::class, 'MaHSO', 'MaHSO');
    }

    public function kqHocTaps(): HasMany
    {
        return $this->hasMany(\App\Modules\HocTap\Models\KQHocTap::class, 'MaSV', 'MaSV');
    }

    public function totNghiep(): HasMany
    {
        return $this->hasMany(\App\Modules\TotNghiep\Models\TotNghiep::class, 'MaSV', 'MaSV');
    }

    public function tbNguoiNhans(): HasMany
    {
        return $this->hasMany(\App\Modules\ThongBao\Models\TBNguoiNhan::class, 'MaSV', 'MaSV');
    }
}
