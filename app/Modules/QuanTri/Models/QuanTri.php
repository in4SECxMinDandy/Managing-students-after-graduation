<?php

namespace App\Modules\QuanTri\Models;

use App\Modules\Core\BaseModel;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Laravel\Sanctum\HasApiTokens;

class QuanTri extends Authenticatable
{
    use HasApiTokens;

    protected $table = 'quan_tri';

    protected $primaryKey = 'MaAdmin';

    public $incrementing = false;

    protected $keyType = 'string';

    public $timestamps = false;

    protected $fillable = ['MaAdmin', 'TenDN', 'MatKhau'];

    protected $hidden = ['MatKhau'];

    protected $casts = [
        'TenDN'   => 'string',
        'MatKhau' => 'string',
    ];

    public function getAuthPassword(): string
    {
        return $this->MatKhau;
    }

    public function thongBaos(): HasMany
    {
        return $this->hasMany(\App\Modules\ThongBao\Models\ThongBao::class, 'MaAdmin', 'MaAdmin');
    }

    public function ptxetTuyens(): HasMany
    {
        return $this->hasMany(\App\Modules\TuyenSinh\Models\PTXetTuyen::class, 'MaAdmin', 'MaAdmin');
    }
}
