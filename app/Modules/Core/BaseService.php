<?php

namespace App\Modules\Core;

use Illuminate\Support\ServiceProvider;

abstract class BaseService
{
    protected static string $model;

    public function __construct()
    {
        if (static::$model && class_exists(static::$model)) {
            $this->model = app(static::$model);
        }
    }

    public function getModel(): string
    {
        return static::$model;
    }

    public function all(array $columns = ['*'])
    {
        return static::$model::all($columns);
    }

    public function find(int|string $id)
    {
        return static::$model::find($id);
    }

    public function create(array $data)
    {
        return static::$model::create($data);
    }

    public function update(int|string $id, array $data): bool
    {
        return static::$model::find($id)?->update($data);
    }

    public function delete(int|string $id): bool
    {
        return static::$model::find($id)?->delete();
    }

    public function paginate(int $perPage = 15, array $columns = ['*'])
    {
        return static::$model::paginate($perPage, $columns);
    }
}
