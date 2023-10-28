
from attr import dataclass
import glm
from component.floor_hull_component import FloorHullComponent
from component.hull_component import HullComponent
from component.sphere_hull_component import SphereHullComponent
from component.transform_component import TransformComponent
from gfx.transform import Transform
from scene.scene_object import SceneObject


@dataclass
class CollisionResult:
    obj_a: SceneObject = None
    obj_b: SceneObject = None
    hit_a: glm.vec3 = glm.vec3(0)
    hit_b: glm.vec3 = glm.vec3(0)
    penetration: float = 0
    hit_normal: glm.vec3 = glm.vec3(0)
    is_hit: bool = False


class CollisionTests:

    def test_collision(obj_a: SceneObject, obj_b: SceneObject) -> CollisionResult:
        # check both objects have at least one collision hull
        hulls_a = obj_a.get_components(HullComponent)
        hulls_b = obj_b.get_components(HullComponent)
        if len(hulls_a) == 0 or len(hulls_b) == 0: return CollisionResult()

        # get transform of each object, return if either have none
        trans_a = obj_a.get_component(TransformComponent)
        trans_b = obj_b.get_component(TransformComponent)
        if trans_a is None or trans_b is None: return CollisionResult()

        for hull_a in hulls_a:
            for hull_b in hulls_b:

                # determine type of each hull to perform correct collision detection
                # TODO: i'm sure there is a better way to do this, haven't put much thought in to it yet

                if isinstance(hull_a, SphereHullComponent) and isinstance(hull_b, SphereHullComponent):
                    return CollisionTests._test_collision_sphere_sphere(obj_a,
                                                                        trans_a.transform,
                                                                        hull_a,
                                                                        obj_b,
                                                                        trans_b.transform,
                                                                        hull_b)
                elif isinstance(hull_a, SphereHullComponent) and isinstance(hull_b, FloorHullComponent):
                    return CollisionTests._test_collision_sphere_floor(obj_a,
                                                                       trans_a.transform,
                                                                       hull_a,
                                                                       obj_b,
                                                                       trans_b.transform,
                                                                       hull_b)
                elif isinstance(hull_a, FloorHullComponent) and isinstance(hull_b, SphereHullComponent):
                    return CollisionTests._test_collision_sphere_floor(obj_b,
                                                                       trans_b.transform,
                                                                       hull_b,
                                                                       obj_a,
                                                                       trans_a.transform,
                                                                       hull_a)

                else:
                    raise Exception("invalid collision pair")

        return CollisionResult()

    def _test_collision_sphere_sphere(obj_a: SceneObject,
                                      trans_a: Transform,
                                      hull_a: SphereHullComponent,
                                      obj_b: SceneObject,
                                      trans_b: Transform,
                                      hull_b: SphereHullComponent) -> CollisionResult:

        # distance between the two objects
        dist = glm.distance(trans_a.position, trans_b.position)
        # check if distance is less than sum of radii
        if dist <= hull_a.radius + hull_b.radius:
            hit_a = trans_a.position + glm.normalize(trans_b.position - trans_a.position) * hull_a.radius
            hit_b = trans_b.position + glm.normalize(trans_a.position - trans_b.position) * hull_b.radius
            normal = glm.normalize(hit_b - hit_a)
            penetration = abs(glm.length(hit_b - hit_a))
            return CollisionResult(hit_a=hit_a, hit_b=hit_b, hit_normal=normal, is_hit=True, obj_a=obj_a, obj_b=obj_b, penetration=penetration)

        # if no collision, return default 'no hit' result
        return CollisionResult()

    def _test_collision_sphere_floor(obj_a: SceneObject,
                                     trans_a: Transform,
                                     hull_a: SphereHullComponent,
                                     obj_b: SceneObject,
                                     trans_b: Transform,
                                     hull_b: FloorHullComponent) -> CollisionResult:

        # distance between bottom (lowest Y) of sphere and floor height
        dist = trans_a.position.y - (hull_b.height + trans_b.position.y)
        if dist <= hull_a.radius:
            # NOTE: i'm not sure how accurate this is
            hit_a = trans_a.position + glm.vec3(0, -hull_a.radius, 0)
            hit_b = hit_a
            normal = glm.vec3(0, 1, 0)
            penetration = abs((hull_b.height + trans_b.position.y) - hit_a.y)
            return CollisionResult(hit_a=hit_a, hit_b=hit_b, hit_normal=normal, is_hit=True, obj_a=obj_a, obj_b=obj_b, penetration=penetration)

        # if no collision, return default 'no hit' result
        return CollisionResult()
