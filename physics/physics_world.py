
from typing import Self

import glm
from component.rigid_body_component import RigidBodyComponent
from component.transform_component import TransformComponent
from physics.collision_tests import CollisionResult, CollisionTests
from physics.solvers.solver import Solver

from scene.scene_object import SceneObject


class PhysicsWorld:
    """
    Handles all physics interactions between objects
    """

    def __init__(self: Self) -> None:
        self.objects: list[SceneObject] = []  # SceneObjects registered for physics shizzle
        self.solvers: list[Solver] = []  # global physics solvers (gravity, wind etc)
        pass

    def physics_tick(self: Self, delta: float) -> None:
        # run all solvers
        self.solve(delta)
        # get all collisions
        collisions = self.detect_collisions()
        # resolve all found collisions
        self.resolve_collisions(collisions)

    def solve(self: Self, delta: float) -> None:
        for solver in self.solvers:
            for obj in self.objects:
                # run each solver on every registered object
                solver.solve(obj, delta)

    def detect_collisions(self: Self) -> list[CollisionResult]:
        result: list[CollisionResult] = []

        # keep track of objects that have been tested for collision
        # no need to test collisions between the same objects twice
        tested_pairs: dict[SceneObject, list[SceneObject]] = {}

        # for each obj in the world...
        for obj_a in self.objects:
            if obj_a not in tested_pairs:
                tested_pairs[obj_a] = []
            # test against every other object in the world...
            for obj_b in self.objects:
                if obj_b not in tested_pairs:
                    tested_pairs[obj_b] = []
                if obj_a == obj_b: continue  # don't check collision if objects are same
                if obj_b in tested_pairs[obj_a]: continue  # don't check if the pair has already been tested

                # mark this pair as having been tested
                tested_pairs[obj_a].append(obj_b)
                tested_pairs[obj_b].append(obj_a)

                # test the collision
                collision = CollisionTests.test_collision(obj_a, obj_b)

                # if collision test is a hit, add it to the list of collisions
                if collision.is_hit:
                    result.append(collision)

        # returns all hit collisions
        return result

    def resolve_collisions(self: Self, collisions: list[CollisionResult]) -> None:
        for collision in collisions:

            rb_a = collision.obj_a.get_component(RigidBodyComponent)
            trans_a = collision.obj_a.get_component(TransformComponent)
            rb_b = collision.obj_b.get_component(RigidBodyComponent)
            trans_b = collision.obj_b.get_component(TransformComponent)

            relative_velocity = rb_b.velocity - rb_a.velocity

            if rb_a.mass > 0 and rb_b.mass > 0:
                sep_a = collision.penetration * (rb_b.mass / (rb_a.mass + rb_b.mass))
                sep_b = collision.penetration * (rb_a.mass / (rb_a.mass + rb_b.mass))
                trans_a.translate(collision.hit_normal * sep_a)
                trans_b.translate(-collision.hit_normal * sep_b)
                impulse_magnitude = glm.dot(relative_velocity, collision.hit_normal) / (1 / rb_a.mass + 1 / rb_b.mass)
                rb_a.impulse(impulse_magnitude * collision.hit_normal * rb_a.get_restitution() * 2.0)
                rb_b.impulse(-impulse_magnitude * collision.hit_normal * rb_b.get_restitution() * 2.0)
            elif rb_a.mass > 0:
                sep_a = collision.penetration
                trans_a.translate(collision.hit_normal * sep_a)
                impulse_magnitude = -2.0 * glm.dot(relative_velocity, collision.hit_normal) / (1 / rb_a.mass)
                rb_a.impulse(-impulse_magnitude * collision.hit_normal * rb_a.get_restitution())
            elif rb_b.mass > 0:
                sep_b = collision.penetration
                trans_b.translate(collision.hit_normal * sep_b)
                impulse_magnitude = -2.0 * glm.dot(relative_velocity, collision.hit_normal) / (1 / rb_b.mass)
                rb_b.impulse(impulse_magnitude * collision.hit_normal * rb_b.get_restitution())

    def add_solver(self: Self, solver: Solver) -> None:
        self.solvers.append(solver)

    def register_object(self: Self, object: SceneObject) -> None:
        self.objects.append(object)
