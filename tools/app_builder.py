
import shader_compiler as sc


def compile_shaders() -> None:
    sc.compile(["shaders/fbo_draw.frag", "shaders/fbo_draw.vert"], "assets/shader/fbo_draw.shader")
    sc.compile(["shaders/geometry.frag", "shaders/geometry.vert"], "assets/shader/geometry.shader")
    sc.compile(["shaders/shading.frag", "shaders/shading.vert"], "assets/shader/shading.shader")
    sc.compile(["shaders/light_pass.frag", "shaders/light_pass.vert"], "assets/shader/light_pass.shader")
    sc.compile(["shaders/pbr_shader.frag", "shaders/pbr_shader.vert"], "assets/shader/pbr_shader.shader")
    pass


def main() -> None:
    compile_shaders()
    pass


if __name__ == "__main__":
    main()
