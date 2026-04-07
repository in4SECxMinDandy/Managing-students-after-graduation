<?php

namespace App\Modules\TuyenSinh\Models;

use App\Modules\Core\BaseModel;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Laravel\Sanctum\HasApiTokens;

class TKXetTuyen extends Authenticatable
{
    use HasApiTokens;

    protected $table = 'tk_xet_tuyen';

    protected $primaryKey = 'MaTK';

    public $incrementing = false;

    protected $keyType = 'string';

    public $timestamps = false;

    protected $fillable = ['MaTK', 'Email', 'MatKhau'];

    protected $hidden = ['MatKhau'];

    protected $casts = [
        'Email'   => 'string',
        'MatKhau' => 'string',
    ];

    public function getAuthPassword(): string
    {
        return $this->MatKhau;
    }

    public function hsoXetTuyen(): HasMany
    {
        return $this->hasMany(HSOXetTuyen::class, 'MaTK', 'MaTK');
    }
}
