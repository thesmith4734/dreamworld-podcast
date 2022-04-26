import { createTheme, responsiveFontSizes } from '@material-ui/core/styles';

let theme = createTheme({
    palette: {
        primary: {
            main: '#2B4162'
        },
        secondary: {
            main: '#385F71'
        },
        divider: '#385F71',
        text: {
            primary: '#F5F0F6',
            secondary: '#F5F0F6'
        }
    },
});

theme = responsiveFontSizes(theme);

export default theme;