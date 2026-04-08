<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Danh sách Ngành</h2>
    <table class="w-full bg-white rounded-lg shadow overflow-hidden">
        <thead class="bg-green-900 text-white">
            <tr>
                <th class="px-6 py-3 text-left">Mã Ngành</th>
                <th class="px-6 py-3 text-left">Tên Ngành</th>
                <th class="px-6 py-3 text-left">Khoa</th>
            </tr>
        </thead>
        <tbody>
            <?php if(\Livewire\Mechanisms\ExtendBlade\ExtendBlade::isRenderingLivewireComponent()): ?><!--[if BLOCK]><![endif]--><?php endif; ?><?php $__empty_1 = true; $__currentLoopData = $nganhs; $__env->addLoop($__currentLoopData); foreach($__currentLoopData as $nganh): $__env->incrementLoopIndices(); $loop = $__env->getLastLoop(); $__empty_1 = false; ?>
                <tr class="border-b hover:bg-gray-50">
                    <td class="px-6 py-3 font-medium"><?php echo e($nganh['ma_nganh']); ?></td>
                    <td class="px-6 py-3"><?php echo e($nganh['ten_nganh']); ?></td>
                    <td class="px-6 py-3"><?php echo e($nganh['khoa']['ten_khoa'] ?? 'N/A'); ?></td>
                </tr>
            <?php endforeach; $__env->popLoop(); $loop = $__env->getLastLoop(); if ($__empty_1): ?>
                <tr>
                    <td colspan="3" class="px-6 py-4 text-center text-gray-500">Chưa có ngành nào.</td>
                </tr>
            <?php endif; ?><?php if(\Livewire\Mechanisms\ExtendBlade\ExtendBlade::isRenderingLivewireComponent()): ?><!--[if ENDBLOCK]><![endif]--><?php endif; ?>
        </tbody>
    </table>
</div>
<?php /**PATH C:\Users\haqua\Documents\GitHub\QLSVSDH\resources\views/livewire/nganh/index.blade.php ENDPATH**/ ?>