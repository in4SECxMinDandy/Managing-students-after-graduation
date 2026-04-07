<?php

namespace App\Modules\ThongBao\Models;

use App\Modules\Core\BaseModel;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class ThongBao extends BaseModel
{
    protected $table = 'thong_bao';

    protected $primaryKey = 'MaTB';

    public $incrementing = false;

    protected $keyType = 'string';

    public $timestamps = false;

    protected $fillable = ['MaTB', 'NoiDung', 'NgayGui', 'MaAdmin'];

    protected $casts = [
        'NoiDung'  => 'string',
        'NgayGui'  => 'date',
        'MaAdmin'  => 'string',
    ];

    public function quanTri(): BelongsTo
    {
        return $this->belongsTo(\App\Modules\QuanTri\Models\QuanTri::class, 'MaAdmin', 'MaAdmin');
    }

    public function tbNguoiNhans(): HasMany
    {
        return $this->hasMany(TBNguoiNhan::class, 'MaTB', 'MaTB');
    }
}
