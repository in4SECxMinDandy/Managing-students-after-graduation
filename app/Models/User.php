<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;

/**
 * Stub model for config/auth.php default `users` provider.
 * This app authenticates via QuanTri / SinhVien / TKXetTuyen guards.
 */
class User extends Authenticatable
{
    use HasFactory;

    protected $guarded = [];
}
