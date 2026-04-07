<?php

namespace App\Modules\ThongBao\Models;

use App\Modules\Core\BaseModel;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class TBNguoiNhan extends BaseModel
{
    protected $table = 'tb_nguoi_nhan';

    public $incrementing = true;

    protected $fillable = ['MaTB', 'MaSV', 'TrangThaiDoc', 'ThoiGianDoc'];

    protected $casts = [
        'TrangThaiDoc' => 'boolean',
        'ThoiGianDoc'  => 'date',
    ];

    public $timestamps = false;

    public function thongBao(): BelongsTo
    {
        return $this->belongsTo(ThongBao::class, 'MaTB', 'MaTB');
    }

    public function sinhVien(): BelongsTo
    {
        return $this->belongsTo(\App\Modules\SinhVien\Models\SinhVien::class, 'MaSV', 'MaSV');
    }
}
