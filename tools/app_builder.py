
import shader_compiler as sc


def compile_shaders() -> None:
    sc.compile(["shaders/fbo_blit.frag", "shaders/fbo_blit.vert"], "assets/shader/fbo_blit.shader")
    sc.compile(["shaders/geometry.frag", "shaders/geometry.vert"], "assets/shader/geometry.shader")
    sc.compile(["shaders/shading.frag", "shaders/shading.vert"], "assets/shader/shading.shader")
    sc.compile(["shaders/light_pass.frag", "shaders/light_pass.vert"], "assets/shader/light_pass.shader")
    sc.compile(["shaders/pbr_shader.frag", "shaders/pbr_shader.vert"], "assets/shader/pbr_shader.shader")
    sc.compile(["shaders/basic_shading.frag", "shaders/basic_shading.vert"], "assets/shader/basic_shading.shader")
    sc.compile(["shaders/depth_shader.frag", "shaders/depth_shader.vert"], "assets/shader/depth_shader.shader")
    sc.compile(["shaders/albedo_only.frag", "shaders/albedo_only.vert"], "assets/shader/albedo_only.shader")
    sc.compile(["shaders/skybox.frag", "shaders/skybox.vert"], "assets/shader/skybox.shader")
    sc.compile(["tests/games/pong/shaders/scene.frag", "tests/games/pong/shaders/scene.vert"], "assets/shader/pong_scene.shader")
    sc.compile(["tests/games/pong/shaders/pong_post.frag", "tests/games/pong/shaders/pong_post.vert"], "assets/shader/pong_post.shader")
    pass


def main() -> None:
    compile_shaders()
    pass


if __name__ == "__main__":
    main()
