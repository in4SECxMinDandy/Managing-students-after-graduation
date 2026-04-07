<?php

namespace App\Modules\Core;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

abstract class BaseModel extends Model
{
    use SoftDeletes;

    protected $primaryKey;

    public $incrementing = true;

    protected $keyType = 'string';

    protected function casts(): array
    {
        return [];
    }

    public static function getTableName(): string
    {
        return (new static)->getTable();
    }
}
