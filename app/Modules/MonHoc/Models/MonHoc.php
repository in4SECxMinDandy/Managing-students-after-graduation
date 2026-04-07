<?php

namespace App\Modules\MonHoc\Models;

use App\Modules\Core\BaseModel;
use Illuminate\Database\Eloquent\Relations\HasMany;

class MonHoc extends BaseModel
{
    protected $table = 'mon_hoc';

    protected $primaryKey = 'MaMH';

    public $incrementing = false;

    protected $keyType = 'string';

    public $timestamps = false;

    protected $fillable = ['MaMH', 'TenMH', 'SoTinChi'];

    protected $casts = [
        'TenMH'    => 'string',
        'SoTinChi' => 'integer',
    ];

    public function kqHocTaps(): HasMany
    {
        return $this->hasMany(\App\Modules\HocTap\Models\KQHocTap::class, 'MaMH', 'MaMH');
    }
}
