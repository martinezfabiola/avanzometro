/*
 *  Archivo: estSchema.sql
 *
 *  Contenido:
 *          Scrit de creación de la base de datos de estudiantes.
 *
 *  Creado por:
 *          Prof. Edna RUCKHAUS
 *          UNIVERSIDAD SIMÓN BOLÍVAR
 *  Fecha:  24 de Octubre de 2010
 *
 *  Modificado por:
 *          Prof. Leonid TINEO
 *          UNIVERSIDAD SIMÓN BOLÍVAR
 *  Fecha:  12 de noviembre de 2014
 */
 

/*  Definicion de tablas, sus claves primarias y restricciones de nulidad  */

CREATE TABLE ESTUDIANTE(
        carnet         VARCHAR(7)   NOT NULL,
        cohorte        NUMERIC(4)   NOT NULL,
        nombre        VARCHAR(60)  NOT NULL,
        CONSTRAINT PK_ESTUDIANTE PRIMARY KEY(carnet)
);

CREATE TABLE CURSA(
        id INTEGER NOT NULL,
        carnet VARCHAR(7) NOT NULL,
        codasig CHAR(6) NOT NULL,
        trimestre NUMERIC(1) NOT NULL,
        anio NUMERIC(4) NOT NULL,
        estado VARCHAR(10) NOT NULL, 
        nota NUMERIC(1) NOT NULL,
        CONSTRAINT PK_CURSA PRIMARY KEY (carnet,codasig,trimestre,anio)
);

CREATE TABLE ASIGNATURA(
        codasig CHAR(6) NOT NULL,
        nomasig VARCHAR(50) NOT NULL,
        creditos NUMERIC(2) NOT NULL,
        CONSTRAINT PK_ASIGNATURA PRIMARY KEY(codasig)
);


/* Declaracion de las claves foraneas de las relaciones en el esquema */


/* Claves foraneas de la relacion CURSA */
ALTER TABLE CURSA ADD 
    CONSTRAINT FK_CURSA_ESTUDIANTE FOREIGN KEY (carnet) 
        REFERENCES ESTUDIANTE;

ALTER TABLE CURSA ADD 
    CONSTRAINT FK_CURSA_ASIGNATURA FOREIGN KEY (codasig) 
        REFERENCES ASIGNATURA;

/* QUERY PARA EL PROYECTO */

SELECT sum(creditos), id, cursa.carnet, estado FROM asignatura, cursa, estudiante WHERE asignatura.codasig = cursa.codasig AND cursa.carnet = estudiante.carnet AND cursa.estado = 'aprobado' AND estudiante.cohorte = '2013' GROUP BY cursa.carnet, estado, id


SELECT sum(creditos), id, cursa.carnet, estado FROM asignatura, cursa, estudiante WHERE asignatura.codasig = cursa.codasig AND cursa.carnet = estudiante.carnet AND cursa.estado = 'aprobado' AND estudiante.cohorte = '2014' AND estudiante.carrera = '1700' AND cursa.anio <= 2015 AND (cursa.anio < 2015 OR cursa.trimestre <=4) GROUP BY cursa.carnet, estado, id ORDER BY sum;

SELECT DISTINCT id, cursa.carnet FROM cursa, estudiante WHERE cursa.carnet = estudiante.carnet AND estudiante.cohorte = "+cohorteQuery+" AND estudiante.carrera = "+carreraQuery+" AND cursa.anio <= "+anioQuery+" AND (cursa.anio < "+anioQuery+" OR cursa.trimestre <= "+trimQuery+") GROUP BY cursa.carnet, id;


SELECT DISTINCT id, cursa.carnet FROM cursa, estudiante WHERE cursa.carnet = estudiante.carnet AND estudiante.cohorte = 2014 AND estudiante.carrera = 1700 AND cursa.anio <= 2015 AND (cursa.anio < 2015 OR cursa.trimestre <= 4) GROUP BY cursa.carnet, id;









