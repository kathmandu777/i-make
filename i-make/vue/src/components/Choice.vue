<template>
    <div v-for="(choiceImagesPath, i) in choiceImagesPaths" :key="i">
        <input :id="i" type="checkbox" :value="choiceImagesPath" v-model="selectedChoiceImagesPath">
        <label :for="i"> <img v-bind:src="choiceImagesPath" width="128" height="128">
        </label>
    </div>
    <button id="choice_button" v-on:click="confirm">confirm</button>
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
