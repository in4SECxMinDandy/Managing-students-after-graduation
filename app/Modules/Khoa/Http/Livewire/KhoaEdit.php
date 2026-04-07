<?php

namespace App\Modules\Khoa\Http\Livewire;

use App\Modules\Khoa\Models\Khoa;
use App\Modules\Khoa\Services\KhoaService;
use Livewire\Component;

class KhoaEdit extends Component
{
    public string $maKhoa;
    public string $tenKhoa;

    protected array $rules = [
        'tenKhoa' => 'required|string|max:100|unique:khoa,TenKhoa',
    ];

    protected array $messages = [
        'tenKhoa.required' => 'Tên khoa là bắt buộc.',
        'tenKhoa.unique' => 'Tên khoa đã tồn tại.',
    ];

    public function mount(string $id)
    {
        $this->maKhoa = $id;
        $khoa = Khoa::find($id);
        $this->tenKhoa = $khoa?->TenKhoa ?? '';
    }

    public function update(KhoaService $service)
    {
        $this->validate();
        $service->update($this->maKhoa, ['TenKhoa' => $this->tenKhoa]);
        session()->flash('success', 'Cập nhật thành công!');
    }

    public function render()
    {
        return view('livewire.khoa.edit')
            ->extends('layouts.app')
            ->section('content');
    }
}
