<?php

namespace App\Modules\TotNghiep\Models;

use App\Modules\Core\BaseModel;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class TotNghiep extends BaseModel
{
    protected $table = 'tot_nghiep';

    protected $primaryKey = 'MaSV';

    public $incrementing = false;

    protected $keyType = 'string';

    protected $fillable = ['MaSV', 'GPA', 'XepLoai'];

    protected $casts = [
        'GPA'      => 'decimal:2',
        'XepLoai'  => 'string',
    ];

    public $timestamps = false;

    public const XUAT_SAC   = 'Xuất sắc';
    public const GIOI       = 'Giỏi';
    public const KHA        = 'Khá';
    public const TRUNG_BINH = 'Trung bình';
    public const YEU        = 'Yếu';

    public static function tinhXepLoai(float $gpa): string
    {
        return match (true) {
            $gpa >= 3.60 => self::XUAT_SAC,
            $gpa >= 3.20 => self::GIOI,
            $gpa >= 2.50 => self::KHA,
            $gpa >= 2.00 => self::TRUNG_BINH,
            default      => self::YEU,
        };
    }

    public function sinhVien(): BelongsTo
    {
        return $this->belongsTo(\App\Modules\SinhVien\Models\SinhVien::class, 'MaSV', 'MaSV');
    }
}
