<?php

namespace App\Modules\TuyenSinh\Models;

use App\Modules\Core\BaseModel;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class PTXetTuyen extends BaseModel
{
    protected $table = 'pt_xet_tuyen';

    protected $primaryKey = 'MaPTXT';

    public $incrementing = false;

    protected $keyType = 'string';

    public $timestamps = false;

    protected $fillable = [
        'MaPTXT', 'MaNganh', 'PhuongThuc', 'Diem', 'TrangThai', 'MaHSO', 'MaAdmin',
    ];

    protected $casts = [
        'PhuongThuc' => 'string',
        'Diem'       => 'decimal:2',
        'TrangThai'  => 'string',
    ];

    public const TRANG_THAI_CHO_DUYET = 'Chờ duyệt';
    public const TRANG_THAI_DAU       = 'Đậu';
    public const TRANG_THAI_ROT       = 'Rớt';

    public function hsoXetTuyen(): BelongsTo
    {
        return $this->belongsTo(HSOXetTuyen::class, 'MaHSO', 'MaHSO');
    }

    public function nganh(): BelongsTo
    {
        return $this->belongsTo(\App\Modules\Nganh\Models\Nganh::class, 'MaNganh', 'MaNganh');
    }

    public function quanTri(): BelongsTo
    {
        return $this->belongsTo(\App\Modules\QuanTri\Models\QuanTri::class, 'MaAdmin', 'MaAdmin');
    }
}
