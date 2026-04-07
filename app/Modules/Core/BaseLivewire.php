<?php

namespace App\Modules\Core;

use Livewire\Component;

abstract class BaseLivewire extends Component
{
    protected string $layout = 'layouts.app';

    protected $pageTitle = '';

    protected array $listeners = [];

    public function mount(): void
    {
        //
    }

    public function getLayout(): string
    {
        return $this->layout;
    }

    public function getPageTitle(): string
    {
        return $this->pageTitle;
    }

    protected function success(string $message = 'Thao tác thành công!'): void
    {
        session()->flash('success', $message);
    }

    protected function error(string $message = 'Đã xảy ra lỗi!'): void
    {
        session()->flash('error', $message);
    }
}
