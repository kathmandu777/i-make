<template>
    <div :style="{ position: 'relative' }">
        <div :style="{ position: 'absolute', left: '50%' }">
            <div v-for="(choiceImagesPath, i) in choiceImagesPaths" :key="i" :style="{ position: 'relative' }">
                <input :id="i" type="radio" name="image" :value="choiceImagesPath" v-model="selectedChoiceImagesPath" :style="{ position: 'absolute', top: '40px' }" v-on:change="confirm">
                <label :for="i" >
                    <img v-bind:src="choiceImagesPath" width="128" height="128">
                </label>
            </div>
        </div>
    </div>
    <!-- <div class="container">
        <p>hi</p>
    </div> -->
</template>

<script>
export default {
    name: 'Choice',
    data: function () {
        return {
            choiceImagesPaths: [],
            selectedChoiceImagesPath: [],
        }
    },
    methods: {
        async getChoiceImagesPaths() {
            this.choiceImagesPaths=await window.eel.get_choice_images()()
        },
        async confirm() {
            await window.eel.set_skin_color(27.0, 36.0, 100.0)() // TODO: 任意の色を指定できるように
            await window.eel.set_effect_image_from_path(this.selectedChoiceImagesPath)()
            await window.eel.start()
        }
    },
    mounted: function () {
        this.getChoiceImagesPaths()
    }
}
</script>

<style>
.container {
    height: 100%;
    width: 100%;
}
</style>