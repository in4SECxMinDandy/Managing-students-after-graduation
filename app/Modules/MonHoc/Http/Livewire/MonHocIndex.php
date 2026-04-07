<?php

namespace App\Modules\MonHoc\Http\Livewire;

use App\Modules\MonHoc\Models\MonHoc;
use Livewire\Component;

class MonHocIndex extends Component
{
    public array $monHocs = [];

    public function mount()
    {
        $this->monHocs = MonHoc::all()->toArray();
    }

    public function render()
    {
        return view('livewire.mon-hoc.index')
            ->extends('layouts.app')
            ->section('content');
    }
}
