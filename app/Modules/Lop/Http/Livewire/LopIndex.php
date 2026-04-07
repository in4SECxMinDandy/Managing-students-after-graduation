<?php

namespace App\Modules\Lop\Http\Livewire;

use App\Modules\Lop\Models\Lop;
use App\Modules\Nganh\Models\Nganh;
use Livewire\Component;

class LopIndex extends Component
{
    public array $lops = [];
    public array $nganhs = [];

    public function mount()
    {
        $this->lops = Lop::with('nganh')->get()->toArray();
        $this->nganhs = Nganh::all()->toArray();
    }

    public function render()
    {
        return view('livewire.lop.index')
            ->extends('layouts.app')
            ->section('content');
    }
}
