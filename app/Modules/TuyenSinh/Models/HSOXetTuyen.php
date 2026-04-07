<?php

namespace App\Modules\TuyenSinh\Models;

use App\Modules\Core\BaseModel;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class HSOXetTuyen extends BaseModel
{
    protected $table = 'hso_xet_tuyen';

    protected $primaryKey = 'MaHSO';

    public $incrementing = false;

    protected $keyType = 'string';

    public $timestamps = false;

    protected $fillable = ['MaHSO', 'MaTK', 'HoTen', 'CCCD', 'SDT'];

    protected $casts = [
        'HoTen' => 'string',
        'CCCD'  => 'string',
        'SDT'   => 'string',
    ];

    public function tkXetTuyen(): BelongsTo
    {
        return $this->belongsTo(TKXetTuyen::class, 'MaTK', 'MaTK');
    }

    public function sinhVien(): HasMany
    {
        return $this->hasMany(\App\Modules\SinhVien\Models\SinhVien::class, 'MaHSO', 'MaHSO');
    }

    public function ptXetTuyens(): HasMany
    {
        return $this->hasMany(PTXetTuyen::class, 'MaHSO', 'MaHSO');
    }
}
