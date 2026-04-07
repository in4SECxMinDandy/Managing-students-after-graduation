<?php

namespace App\Modules\Nganh\Http\Livewire;

use App\Modules\Nganh\Models\Nganh;
use App\Modules\Khoa\Models\Khoa;
use Livewire\Component;

class NganhIndex extends Component
{
    public array $nganhs = [];
    public array $khoas = [];

    public function mount()
    {
        $this->nganhs = Nganh::with('khoa')->get()->toArray();
        $this->khoas = Khoa::all()->toArray();
    }

    public function render()
    {
        return view('livewire.nganh.index')
            ->extends('layouts.app')
            ->section('content');
    }
}
