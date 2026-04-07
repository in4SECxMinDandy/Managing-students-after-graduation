<?php

namespace App\Modules\Core;

use Illuminate\Support\ServiceProvider;

class CoreServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->loadMigrationsFrom(__DIR__.'/../../Modules/*/Database/Migrations');
    }

    public function boot(): void
    {
        //
    }
}
