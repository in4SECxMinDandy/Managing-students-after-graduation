<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Đăng nhập Sinh viên</h2>

    <form wire:submit="login">
        <div class="mb-4">
            <label class="block text-gray-700 font-medium mb-2">Mã sinh viên</label>
            <input type="text" wire:model="maSV"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="VD: SV2600000001">
            @error('maSV') <span class="text-red-500 text-sm">{{ $message }}</span> @enderror
        </div>

        <div class="mb-6">
            <label class="block text-gray-700 font-medium mb-2">Mật khẩu</label>
            <input type="password" wire:model="password"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
            @error('password') <span class="text-red-500 text-sm">{{ $message }}</span> @enderror
        </div>

        <button type="submit"
            class="w-full bg-green-600 text-white py-2 px-4 rounded-lg hover:bg-green-700 font-medium">
            Đăng nhập
        </button>
    </form>
</div>
