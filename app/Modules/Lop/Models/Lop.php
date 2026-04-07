<?php

namespace App\Modules\Lop\Models;

use App\Modules\Core\BaseModel;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Lop extends BaseModel
{
    protected $table = 'lop';

    protected $primaryKey = 'MaLop';

    public $incrementing = false;

    protected $keyType = 'string';

    public $timestamps = false;

    protected $fillable = ['MaLop', 'TenLop', 'MaNganh'];

    protected $casts = [
        'TenLop'  => 'string',
        'MaNganh' => 'string',
    ];

    public function nganh(): BelongsTo
    {
        return $this->belongsTo(\App\Modules\Nganh\Models\Nganh::class, 'MaNganh', 'MaNganh');
    }

    public function sinhViens(): HasMany
    {
        return $this->hasMany(\App\Modules\SinhVien\Models\SinhVien::class, 'MaLop', 'MaLop');
    }
}
