<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Livewire\Component;
use Livewire\Livewire;

class AppServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        //
    }

    public function boot(): void
    {
        Livewire::resolveMissingComponent(function (string $name) {
            $studlyParts = collect(explode('.', $name))->map(
                fn (string $s) => (string) str($s)->studly()
            );
            $candidates = [
                '\\'.$studlyParts->join('\\'),
                '\\App\\Modules\\'.$studlyParts->join('\\'),
            ];
            foreach ($candidates as $fqcn) {
                if (class_exists($fqcn) && is_subclass_of($fqcn, Component::class)) {
                    return $fqcn;
                }
            }

            return false;
        });
    }
}
