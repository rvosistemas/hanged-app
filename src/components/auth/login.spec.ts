import { shallowMount } from "@vue/test-utils";
import Login from "./LoginForm.vue";
import { describe, it, expect } from 'vitest';

describe("Login", () => {
    it("should render the component", () => {
        const wrapper = shallowMount(Login);

        expect(wrapper.find(".login-container").exists()).toBeTruthy();
    });
});