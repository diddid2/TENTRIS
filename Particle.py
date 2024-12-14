import pygame
from Utils import *
class ParticlePrinciple:
    def __init__(self):
        self.particles = []
    def emit(self, SCREEN, deltaTime):
        if self.particles:
            self.delete_particles()
            for particle in self.particles:
                if particle['TYPE'] == 'BUBBLE':
                    particle['POSITION'][0] += particle['VELOCITY'][0] * deltaTime
                    particle['POSITION'][1] += particle['VELOCITY'][1] * deltaTime
                    particle['RADIUS'] -= 10 * deltaTime
                    pygame.draw.circle(SCREEN, particle['COLOR'],particle['POSITION'], int(particle['RADIUS']))
                if particle['TYPE'] == 'DIRT':
                    MIN_X = MIN_Y = 0
                    MAX_X = MAX_Y = particle['SIZE']
                    particle['ELAPSED_TIME'] += deltaTime
                    particle['ROTATION'] = particle['ELAPSED_TIME'] * particle['ROTATION_VELOCITY']
                    particle['POSITION'][0] += particle['VELOCITY'][0] * deltaTime
                    particle['POSITION'][1] += particle['VELOCITY'][1] * deltaTime
                    particle['VELOCITY'][1] += 9.8 * .4 #1px당 1m 가정시 0.4g의 중력가속도
                    s = pygame.Surface((particle['SIZE'], particle['SIZE']), pygame.SRCALPHA)
                    s.set_alpha(255 * (1-particle['ELAPSED_TIME']/particle['EMIT_TIME']))
                    pygame.draw.polygon(s, particle['COLOR'], get_rotated_polygon([[MIN_X,MIN_Y],[MAX_X,MIN_Y],[MIN_X,MAX_Y]],particle['ROTATION']))
                    SCREEN.blit(s, particle['POSITION'])
                if particle['TYPE'] == 'RESIDUAL':
                    MIN_X = MIN_Y = 0
                    MAX_X, MAX_Y = particle['SIZE'][0], particle['SIZE'][1]
                    particle['ELAPSED_TIME'] += deltaTime
                    if particle['ELAPSED_TIME'] > particle['FRESH_TIME']:
                        particle['ROTATION'] += deltaTime * particle['ROTATION_VELOCITY']
                        particle['POSITION'][0] += particle['VELOCITY'][0] * deltaTime
                        particle['POSITION'][1] += particle['VELOCITY'][1] * deltaTime
                        particle['VELOCITY'][1] += 9.8 * .2
                    s = pygame.Surface((particle['SIZE'][0], particle['SIZE'][1]), pygame.SRCALPHA)
                    pygame.draw.polygon(s, particle['COLOR'], get_rotated_polygon([[MIN_X,MIN_Y],[MIN_Y,MAX_Y],[MAX_X,MAX_Y],[MAX_X,MIN_Y]],particle['ROTATION']))
                    s.set_alpha(60 * (1-particle['ELAPSED_TIME']/(particle['EMIT_TIME'] - particle['FRESH_TIME'])))
                    SCREEN.blit(s, particle['POSITION'])
                if particle['TYPE'] == 'CLENSING':
                    halfTiming = (particle['EMIT_TIME'] - particle['FLASH_TIME']) / 2
                    clensingTime = particle['ELAPSED_TIME'] - particle['FLASH_TIME']
                    DELTA_X = particle['SIZE'][0] / halfTiming * clensingTime
                    DELTA_Y = particle['SIZE'][1] / halfTiming * clensingTime
                    END_X = particle['SIZE'][0]
                    END_Y = particle['SIZE'][1]
                    s = pygame.Surface((particle['SIZE'][0], particle['SIZE'][1]), pygame.SRCALPHA)
                    if particle['ELAPSED_TIME'] < particle['FLASH_TIME']:
                        pygame.draw.rect(s, particle['COLOR'], (0, 0, particle['SIZE'][0], particle['SIZE'][1]))
                    elif particle['ELAPSED_TIME'] - particle['FLASH_TIME'] <= halfTiming:
                        pygame.draw.polygon(s, particle['COLOR'],[[0, DELTA_Y], [DELTA_X, 0], [END_X, 0], [END_X, END_Y], [0, END_Y]])
                    else:
                        pygame.draw.polygon(s, particle['COLOR'], [[END_X, END_Y], [DELTA_X-particle['SIZE'][0],END_Y], [END_X, DELTA_Y-particle['SIZE'][1]]])
                    SCREEN.blit(s, particle['POSITION'])
                    particle['ELAPSED_TIME'] += deltaTime
                if particle['TYPE'] == 'SNOW':
                    if particle['POSITION'][0] > particle['AXIS_X'] + 30:
                        particle['VELOCITY'] = (-abs(particle['VELOCITY'][0]), particle['VELOCITY'][1])
                    if particle['POSITION'][0] < particle['AXIS_X'] - 30:
                        particle['VELOCITY'] = (abs(particle['VELOCITY'][0]),  particle['VELOCITY'][1])
                    particle['VELOCITY'] = (particle['VELOCITY'][0], particle['VELOCITY'][1]+deltaTime * 9.8*10)
                    particle['POSITION'][0] += particle['VELOCITY'][0] * deltaTime
                    particle['POSITION'][1] += particle['VELOCITY'][1] * deltaTime
                    pygame.draw.circle(SCREEN, (114,183,207), particle['POSITION'], int(particle['RADIUS']))
                    pygame.draw.circle(SCREEN, particle['COLOR'], particle['POSITION'], int(particle['RADIUS']-2))

    def add_bubble_particle(self,pos_x,pos_y,radius,velocity, color):
        self.particles.append({'TYPE' : 'BUBBLE', 'POSITION' : [pos_x, pos_y],
                               'RADIUS' : radius, 'VELOCITY' : velocity,
                               'COLOR' : color})

    def add_snow_particle(self,pos_x,pos_y,radius,velocity, color):
        self.particles.append({'TYPE' : 'SNOW', 'POSITION' : [pos_x, pos_y],
                               'RADIUS' : radius, 'VELOCITY' : velocity,
                               'COLOR' : color, 'AXIS_X' : pos_x})

    def add_clensing_particle(self,pos_x,pos_y,size_x,size_y,color,flashTime,emitTime):
        self.particles.append({'TYPE': 'CLENSING', 'POSITION': [pos_x, pos_y],
                               'SIZE': [size_x, size_y], 'COLOR': color,
                               'ELAPSED_TIME': 0.0, 'FLASH_TIME': flashTime,
                               'EMIT_TIME': emitTime})
    def add_dirt_particle(self,pos_x,pos_y,velocity,size,color,rotationvel,emitTime):
        self.particles.append({'TYPE': 'DIRT', 'POSITION': [pos_x,pos_y],
                               'VELOCITY':velocity, 'SIZE': size, 'COLOR': color,
                               'ROTATION_VELOCITY': rotationvel, 'EMIT_TIME': emitTime,
                               'ROTATION': 0, 'ELAPSED_TIME': 0})
    def add_residual_particle(self,pos_x,pos_y,velocity,rotationvel,size,color,fresh_time,emitTime):
        self.particles.append({'TYPE': 'RESIDUAL', 'POSITION': [pos_x, pos_y], 'VELOCITY': velocity,
                               'SIZE': size, 'COLOR': color, 'EMIT_TIME': emitTime, 'FRESH_TIME': fresh_time,
                               'ROTATION': 0, 'ROTATION_VELOCITY': rotationvel, 'ELAPSED_TIME': 0})
    def delete_particles(self):
        particle_copy = []
        for particle in self.particles:
            if particle['TYPE'] == 'BUBBLE' and particle['RADIUS'] > 0:
                particle_copy.append(particle)
            if ((particle['TYPE'] == 'CLENSING' or particle['TYPE'] == 'DIRT' or particle['TYPE'] == 'RESIDUAL')
                    and particle['ELAPSED_TIME'] <= particle['EMIT_TIME']):
                particle_copy.append(particle)
            if particle['TYPE'] == 'SNOW' and particle['POSITION'][1] < 1920:
                particle_copy.append(particle)
        self.particles = particle_copy