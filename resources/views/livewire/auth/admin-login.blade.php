<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Đăng nhập Quản trị</h2>

    <form wire:submit="login">
        <div class="mb-4">
            <label class="block text-gray-700 font-medium mb-2">Tên đăng nhập</label>
            <input type="text" wire:model="tenDN"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            @error('tenDN') <span class="text-red-500 text-sm">{{ $message }}</span> @enderror
        </div>

        <div class="mb-6">
            <label class="block text-gray-700 font-medium mb-2">Mật khẩu</label>
            <input type="password" wire:model="password"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            @error('password') <span class="text-red-500 text-sm">{{ $message }}</span> @enderror
        </div>

        <button type="submit"
            class="w-full bg-gray-800 text-white py-2 px-4 rounded-lg hover:bg-gray-900 font-medium">
            Đăng nhập
        </button>
    </form>
</div>
