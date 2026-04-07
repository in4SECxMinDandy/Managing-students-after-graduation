<?php

namespace App\Modules\Khoa\Models;

use App\Modules\Core\BaseModel;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Khoa extends BaseModel
{
    protected $table = 'khoa';

    protected $primaryKey = 'MaKhoa';

    public $incrementing = false;

    protected $keyType = 'string';

    public $timestamps = false;

    protected $fillable = ['MaKhoa', 'TenKhoa'];

    protected $casts = [
        'TenKhoa' => 'string',
    ];

    public function nganhs(): HasMany
    {
        return $this->hasMany(\App\Modules\Nganh\Models\Nganh::class, 'MaKhoa', 'MaKhoa');
    }
}
