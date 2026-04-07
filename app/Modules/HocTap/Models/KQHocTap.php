<?php

namespace App\Modules\HocTap\Models;

use App\Modules\Core\BaseModel;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class KQHocTap extends BaseModel
{
    protected $table = 'kq_hoc_tap';

    public $incrementing = false;

    protected $keyType = 'string';

    protected $fillable = ['MaSV', 'MaMH', 'Diem'];

    protected $casts = [
        'Diem' => 'decimal:2',
    ];

    public $timestamps = false;

    public function sinhVien(): BelongsTo
    {
        return $this->belongsTo(\App\Modules\SinhVien\Models\SinhVien::class, 'MaSV', 'MaSV');
    }

    public function monHoc(): BelongsTo
    {
        return $this->belongsTo(\App\Modules\MonHoc\Models\MonHoc::class, 'MaMH', 'MaMH');
    }

    public static function compositeKey(): bool
    {
        return true;
    }
}
