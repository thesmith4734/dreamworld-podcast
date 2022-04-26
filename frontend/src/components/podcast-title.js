import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Link } from 'react-router-dom'

const useStyles = makeStyles((theme) => ({
    card: {
        marginBottom: theme.spacing(7),
        marginTop: theme.spacing(7),
        width: '90%',
        height: '50px',
        borderRadius: '5px',
        backgroundColor: '#FBDD96',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    }
}));

export default function PodcastTitle(props) {
    const classes = useStyles();

    return(
        <div className={classes.card}>
            <Link to={`podcasts/${props.url}`}>
                <span>{props.title}</span>
            </Link>
        </div>
    )
}