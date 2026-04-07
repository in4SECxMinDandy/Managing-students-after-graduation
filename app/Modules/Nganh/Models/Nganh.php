<?php

namespace App\Modules\Nganh\Models;

use App\Modules\Core\BaseModel;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Nganh extends BaseModel
{
    protected $table = 'nganh';

    protected $primaryKey = 'MaNganh';

    public $incrementing = false;

    protected $keyType = 'string';

    public $timestamps = false;

    protected $fillable = ['MaNganh', 'TenNganh', 'MaKhoa'];

    protected $casts = [
        'TenNganh' => 'string',
        'MaKhoa'   => 'string',
    ];

    public function khoa(): BelongsTo
    {
        return $this->belongsTo(\App\Modules\Khoa\Models\Khoa::class, 'MaKhoa', 'MaKhoa');
    }

    public function lops(): HasMany
    {
        return $this->hasMany(\App\Modules\Lop\Models\Lop::class, 'MaNganh', 'MaNganh');
    }
}
